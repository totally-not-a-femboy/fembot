import io
from discord.ext import commands
from discord import app_commands
import discord
import aiohttp

class context_menus(commands.Cog):  # All cogs must inherit from commands.Cog
    """A simple, basic cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.context_menu(name="Simp")
    async def simp(interaction: discord.Interaction, user: discord.Member ):
        member = user
        async with aiohttp.ClientSession() as session:
                async with session.get(
                f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar.url.format("png")}'
                ) as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "simpcard.png")
                        em = discord.Embed(
                            title="Simp!",
                            color=0xf1f1f1,
                        )
                        em.set_image(url="attachment://simpcard.png")
                        await interaction.response.send_message(embed=em, file=file)
                    else:
                        await interaction.response.send_message('Simp')
                await session.close()

    @app_commands.context_menu(name="Jail")
    async def jail(interaction: discord.Interaction, user: discord.Member):
        member = user
        async with aiohttp.ClientSession() as session:
                async with session.get(
                f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.url.format("png")}'
                ) as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "jail.png")
                        em = discord.Embed(
                            title="lo agarraron los municipales :c",
                            color=0xf1f1f1,
                        )
                        em.set_image(url="attachment://jail.png")
                        await interaction.response.send_message(embed=em, file=file)
                    else:
                        await interaction.response.send_message('Something went wrong')      
                await session.close()

    @app_commands.context_menu(name="Gay")
    async def gay(interaction: discord.Interaction, user: discord.Member):
        member = user
        async with aiohttp.ClientSession() as session:
                async with session.get(
                f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.url.format("png")}'
            ) as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "gay.png")
                        em = discord.Embed(
                        title="gei",
                        color=0xf1f1f1,
                        )
                        em.set_image(url="attachment://gay.png")
                        await interaction.response.send_message(embed=em, file=file)
                    else:
                        await interaction.response.send_message('gei')
                await session.close()


async def setup(bot):
    await bot.add_cog(context_menus(bot))