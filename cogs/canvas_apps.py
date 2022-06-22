import io
from typing import Optional
from discord import AppCommandType, app_commands
import discord
import aiohttp

class canvas(app_commands.Group):
    def __init__(self):
        super().__init__()

    @app_commands.command(name="horny", description="Horny license just for u")
    @app_commands.describe(member='member to get the avatar of')
    async def horny(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        '''Horny license just for u'''
        member = member or interaction.user
        async with aiohttp.ClientSession() as session:
                async with session.get(
                f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.url.format("png")}'
                ) as af:
                 if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                    title="bonk",
                    color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await interaction.response.send_message(embed=em, file=file)
                 else:
                    await interaction.response.send_message('No horny :(')
                await session.close()

    @app_commands.command(name="simp", description="simp license just for u")
    @app_commands.describe(member='member to get the avatar of')
    async def simp(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        '''simp license just for u'''
        member = member or interaction.user
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

    @app_commands.command(name="jail")
    @app_commands.describe(member='member to get the avatar of')
    async def jail(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        '''aaaa license just for u'''
        member = member or interaction.user
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

    @app_commands.command(name="gay")
    @app_commands.describe(member='member to get the avatar of')
    async def gay(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        '''aaaa license just for u'''
        member = member or interaction.user
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
    bot.tree.add_command(canvas())