import asyncio
import itertools

import discord
import discord.ext.commands as commands
from async_timeout import timeout
from youtube_dl import YoutubeDL
from functools import partial

ytdl_options = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"before_options": "-nostdin", "options": "-vn"}

ytdl = YoutubeDL(ytdl_options)

class VCError(commands.CommandError):
    """Custom Exception class for VC related errors"""


class InvalidVC(VCError):
    """Exception for when a user tries to use a command while in an invalid VC"""


class YTDLSource(discord.PCMVolumeTransformer):


    def __init__(self, source, *, data, requester):
        super().__init__(source)

        self.requester = requester
        self.title = data.get("title")
        self.web_url = data.get("webpage_url")
        self.thumbnail = data.get('thumbnail')
        self.webpage_url = data.get('webpage_url')
        self.uploader = data.get('uploader')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(
        cls,
        ctx: commands.Context,
        search: str,
        *,
        loop: asyncio.AbstractEventLoop,
        download=False,
    ):
        """
        Creates a source.
        """
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:  # Get the first item in a playlist
            data = data["entries"][0]

        embed = discord.Embed(
            title=f"🎧 Song Added to the Queue", description=f'🎹 {data["title"]}'
        )

        await ctx.send(embed=embed, delete_after=4)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {
                "webpage_url": data["webpage_url"],
                "requester": ctx.author,
                "title": data["title"],
            }

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data: dict, *, loop: asyncio.AbstractEventLoop):
        """
        Used to prepare a stream instead of downloading.
        """
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)

class MusicPlayer:
    """
    Class assigned to each guild using the bot for music.
    """

    __slots__ = (
        "bot",
        "_guild",
        "_channel",
        "_cog",
        "queue",
        "next",
        "current",
        "np",
        "volume",
    )

    def __init__(self, ctx: commands.Context):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.np = None  # Now playing message
        self.volume = 0.5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """
        The main player loop.
        """
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout, cancel player and dc
                async with timeout(300):  # Wait 5 mins
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably not downloaded
                # So we should regather
                try:
                    source = await YTDLSource.regather_stream(
                        source, loop=self.bot.loop
                    )
                except Exception as e:
                    await self._channel.send(
                        f":x: Sorry, I couldn't process your song.\n" + f"\n[{e}]\n",
                        delete_after=20,
                    )
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )

            embed=discord.Embed(title=f"", description=f"[{source.title}]({source.web_url}) - {source.uploader}", color=0x00ff00)
            embed.set_author(name=f"Ahora suena", icon_url=f"https://c.tenor.com/B-pEg3SWo7kAAAAC/disk.gif")
            embed.set_footer(text=f"Requested by: {source.requester.name}")
            embed.set_thumbnail(url=source.thumbnail)
            self.np = await self._channel.send(embed=embed)

            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            try:
                source.cleanup()
            except ValueError as ex:
                error_embed = discord.Embed(
                    title="👎 Discord.py Error",
                    description=f"🐍 Discord.py encountered an internal error.\n```{ex.args}```",
                )

                error_embed.set_footer(
                    text="❓ This may be because we're using Discord.py V2.0.0-alpha."
                )

                await self._channel.send(embed=error_embed)

            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """
        Disconnect and clean up the player.
        """
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class music(commands.GroupCog):
    """
    🎵 Contains music commands.
    """

    __slots__ = ("bot", "players")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        """
        Destroys the music player and disconnects from a voice channel.
        """
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx: commands.Context):
        """
        Local check for all the commands in the cog.
        """
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx: commands.Context, error):
        """
        Error handler for all errors in this cog.
        """
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.reply(
                    f":x: You can't play music in a private message channel.",
                    delete_after=20,
                )
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVC):
            await ctx.reply(
                f":x: Couldn't connect to a VC. "
                + "Please make sure you're in a VC or provide me with one.",
                delete_after=20,
            )

    def get_player(self, ctx: commands.Context):
        """
        Gets the guild player or makes a new one.
        """
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.hybrid_command(name="connect", aliases=["join"])
    async def connect(self, ctx: commands.Context, channel: discord.VoiceChannel = None):
        """
        🎵 Joins a voice channel.
        Usage:
        ```
        ~join [channel]
        ```
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                error_msg = (
                    f":x: No channel to join. Specify a channel or join one yourself."
                )

                await ctx.reply(error_msg, delete_after=20)
                raise AttributeError(error_msg)

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VCError(
                    f":x: Moving to channel **{channel}** timed out.",
                )
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VCError(f":x: Connecting to channel **{channel}** timed out.")

        embed = discord.Embed(
            title=f"🎧 Successfully Connected", description=f"```🎶 Channel: {channel}```"
        )
        embed.set_footer(text="❓ You can use ~del to kick me at any time.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="play", aliases=["p"])
    async def play(self, ctx: commands.Context, *, search: str = None):
        """
        🎵 Plays a song in a voice channel.
        Usage:
        ```
        ~play | ~p <song>
        ```
        """
        async with ctx.typing():
            if not search:
                return await ctx.reply(
                    f":x: You need to specify a song to search for.",
                    delete_after=20,
                )

            vc = ctx.voice_client

            if not vc:
                await ctx.invoke(self.connect)

            player = self.get_player(ctx)
            source = await YTDLSource.create_source(
                ctx, search, loop=self.bot.loop, download=False
            )

            await player.queue.put(source)

    @commands.hybrid_command(name="pause", aliases=["ps"])
    async def pause(self, ctx: commands.Context):
        """
        🎵 Pauses the currently playing song.
        Usage:
        ```
        ~pause | ~ps
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )
        elif vc.is_paused():
            return

        vc.pause()

        embed = discord.Embed(
            title=f"🎧 Paused the Song",
            description=f"⏸️ Paused by **{ctx.author.name}**",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="resume",aliases=["r"])
    async def resume(self, ctx: commands.Context):
        """
        🎵 Resumes the currently playing song.
        Usage:
        ```
        ~resume | ~r
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )

        elif not vc.is_paused():
            return

        vc.resume()

        embed = discord.Embed(
            title=f"🎧 Resumed the Song",
            description=f"▶️ Resumed by **{ctx.author.name}**",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="skip", aliases=["s"])
    async def skip(self, ctx: commands.Context):
        """
        🎵 Skips the currently playing song.
        Usage:
        ```
        ~skip | ~s
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()

        embed = discord.Embed(
            title=f"🎧 Skipped the Song",
            description=f"⏭️ Skipped by **{ctx.author.name}**",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="queue", aliases=["q", "songs"])
    async def queue(self, ctx: commands.Context):
        """
        🎵 Shows the current music queue.
        Usage:
        ```
        ~queue | ~q | ~songs
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(f":x: I'm not connected to VC.", delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.reply(
                f":x: There are no more queued songs.",
                delete_after=20,
            )

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = "\n\n".join(
            f'➡️ **{i + 1}**: {song["title"]}' for i, song in enumerate(upcoming)
        )
        embed = discord.Embed(
            title=f"🎧 Music Queue | {len(upcoming)} Songs",
            description=fmt,
        )

        embed.set_footer(text=f"❓ You can use ~skip to skip to the song at the top.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="nowplaying",aliases=["np"])
    async def nowplaying(self, ctx: commands.Context):
        """
        🎵 Shows the song that's currently playing.
        Usage:
        ```
        ~nowplaying | ~np
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed(
            title=f"🎧 **Now Playing:** *{vc.source.title}*",
            description=f"🎵 Requested by: **{vc.source.requester.name}**",
        )

        player.np = await ctx.send(embed=embed)

    @commands.hybrid_command(name="volume", aliases=["vol"])
    async def volume(self, ctx: commands.Context, *, vol: float):
        """
        🎵 Changes the music player's volume.
        Usage:
        ```
        ~volume | ~vol <volume>
        ```
        """
        vc: discord.VoiceProtocol = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(f":x: I'm not connected to VC.", delete_after=20)

        if not 0 < vol < 101:
            return await ctx.reply(
                f":x: I can only set the volume between 1 and 100.",
                delete_after=20,
            )

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100

        embed = discord.Embed(
            title="🎧 Volume Changed",
            description=f"🔊 **{ctx.author.name}**: Set the volume to *{vol}%*",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="stop",aliases=["del"])
    async def stop(self, ctx: commands.Context):
        """
        🎵 Clears the queue and stops the music player.
        Usage:
        ```
        ~stop | ~del
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.reply(
                f":x: I'm not currently playing anything.",
                delete_after=20,
            )

        await self.cleanup(ctx.guild)


async def setup(bot: commands.Bot):
    await bot.add_cog(music(bot))