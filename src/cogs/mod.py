from ast import alias
import datetime
from sys import excepthook
from discord.ext import commands
from discord import Message
import discord
import asyncio



class mods(commands.Cog):  # All cogs must inherit from commands.Cog
    """A simple, basic cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='purge', help='Elimina los mensajes especificados', aliases=["clear","Clear","CLEAR", "Purge", "PURGE"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount : int = None):
            if amount is None:
                await ctx.send("Ingresa una cantidad valida")
            if amount is not None:
                if amount > 200: 
                    amount = 200
                deleted_messages = await ctx.channel.purge(limit=amount + 1)
                await ctx.send(f"{len(deleted_messages) -1} Mensajes eliminados \n\n Nota:Los mensajes anteriores a 2 semanas no se eliminarán", delete_after=3) # Subtracting 1 as it's the message of the command
        

    @commands.command(name="nuke", aliases=["NUKE", "Nuke"])
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx: commands.Context, channel: discord.TextChannel = None):
        embed1=discord.Embed(title="Nuked the Channel sucessfully!")
        embed1.set_thumbnail(url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1126,w_2000,x_0,y_83/f_auto,q_auto,w_1100/v1555949079/shape/mentalfloss/581049-mesut_zengin-istock-1138195821.jpg")
        embed1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
        embed1.timestamp = datetime.datetime.now()
        embed3=discord.Embed(title="THIS CHANNEL HAS BEEN NUKED! BY THE MOTHER FUCKER URSS FOR THE THIRD WORLD WAR")
        embed3.set_thumbnail(url="https://media0.giphy.com/media/oe33xf3B50fsc/giphy.gif")
        embed3.set_footer(text=f"Nuked by {ctx.author}", icon_url=f"{ctx.author.avatar.url}")
        embed3.timestamp = datetime.datetime.now()
        # getting the message object for editing and reacting 
        if channel is not None:
                    nuke_channel = discord.utils.get(ctx.guild.channels, id=channel.id)
                    if ctx.guild.rules_channel  != nuke_channel:
                        if ctx.guild.public_updates_channel == nuke_channel:
                            await ctx.send("No puedes nukear un canal de la comunidad")
                        if ctx.guild.public_updates_channel != nuke_channel:
                            channel_position = channel.position
                            new_channel = await nuke_channel.clone(reason="Has been Nuked!")
                            await nuke_channel.delete()
                            await new_channel.send(embed=embed3)
                            await new_channel.edit(position=channel_position, sync_permissions=True)
                            await ctx.send(embed=embed1)
                
                    if ctx.guild.rules_channel  == nuke_channel:
                            await ctx.send("No puedes nukear un canal de la comunidad")
        
        if channel is None:
            nuke_channel1 = ctx.channel
            if  ctx.guild.public_updates_channel != nuke_channel1:
                    if ctx.guild.rules_channel == nuke_channel1:
                            await ctx.send("No puedes nukear un canal de la comunidad")
                    if ctx.guild.rules_channel != nuke_channel1:
                        channel_position1 = nuke_channel1.position
                        new_channel1 = await nuke_channel1.clone(reason="Has been Nuked!")
                        await nuke_channel1.delete()
                        await new_channel1.send(embed=embed3)
                        await new_channel1.edit(position=channel_position1, sync_permissions=True)

            if ctx.guild.public_updates_channel == nuke_channel1:
                await ctx.send("No puedes nukear un canal de la comunidad")

    @commands.command(description="Silencia al usuario especificado")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: commands.Context, member: discord.Member = None, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if member is None:
            await ctx.send("Menciona un miembro")

        if member is not None:
            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            await ctx.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(f" Fuiste silenciado en {guild.name} por {reason}")
            await member.remove_roles(member, 'miembro')

    @commands.command(name='ban', help='banea al usuario especificado', aliases=["BAN", "Ban"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx: commands.Context, member : discord.Member = None, *, reason = None):
        await ctx.send("Comando en mantenimiento!")
        """embeds=discord.Embed(title=f"{member} ha sido baneado")
        embeds.set_thumbnail(url="https://cdn.discordapp.com/emojis/944053194907062302.gif?size=240&quality=lossless")
        guild=ctx.guild
        if member is None:
            await ctx.send("Menciona a un miembro")
        if member is not None:
            if member in guild.members:
                try:
                    await member.send(f" Fuiste baneado de {guild.name} por {reason}")
                    await guild.ban(member, reason = reason, delete_message_days=0)
                except:
                        await guild.ban(member, reason = reason, delete_message_days=0)
                        # ending the loop if user doesn't react after x seconds
                await ctx.send(f'{member} fue baneado por {reason}/Moderador {ctx.message.author}') """

    async def cog_command_error(self, ctx, error):
        # Or, if you've already imported `commands`, you could write
        # commands.CommandNotFound here instead of explicitly importing it.
        if isinstance(error, commands.MissingPermissions):  # Using `==` is incorrect
           await ctx.send("No tienes permisos suficientes para usar ese comando")
        
        if isinstance(error, commands.BadArgument):  # Using `==` is incorrect
           await ctx.send("Ingresa una entrada valida")

    @commands.command(name='kick', help='Expulsa al usuario especificado')
    @commands.has_permissions(ban_members = True)
    async def kick(self, ctx: commands.Context, member: discord.Member = None, *, reason=None):
        await ctx.send("Comando en mantenimiento")
        """guild = ctx.guild
        if member is None:
            await ctx.send("Menciona un miembro")

        if member is not None:   
            if ctx.author is guild.owner or ctx.author.top_role >= ctx.guild.me.top_role:
                if ctx.guild.me.top_role <=  member.top_role or member is ctx.guild.owner:  
                    await ctx.send("No puedo expulsar a este usuario")
                if ctx.guild.me.top_role >=  member.top_role or member is not ctx.guild.owner:  
                    if ctx.author.id >= member.top_role or ctx.author.id == guild.owner.id:
                            try:
                                await member.send(f" Fuiste expulsado de {guild.name} por {reason}")
                            except:
                                pass
                            await guild.kick(member, reason=reason)
                            await ctx.send(f'{member} fue expulsado') 
            if ctx.author is not  guild.owner and ctx.author.top_role <= ctx.guild.me.top_role:
                await ctx.send("No puedes expulsar a este usuario")"""


async def setup(bot):
    await bot.add_cog(mods(bot))