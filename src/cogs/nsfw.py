import random
from discord import app_commands
import discord
import requests
import aiohttp
from bs4 import BeautifulSoup
class nsfw(app_commands.Group):  # All cogs must inherit from commands.Cog
    """A simple, basic cog."""
    def __init__(self):
        super().__init__()

    def get_images(self, query):
        """Scrapers the website and extracts image URLs
        Returns:
            imgs [list]: List of image URLs
        """
        url = 'https://rule34.xxx/index.php?page=post&s=list&tags={query}' % query
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find_all('span', class_='thumb')
        imgs = []
        for div in divs:
            img = div.find('img')['src']
            if img.startswith('http'):
                imgs.append(img)
        return imgs

    @app_commands.command(name="neko")
    async def neko(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=False)
        if interaction.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.waifu.pics/nsfw/neko') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        embed = discord.Embed(title='Neko',color=0x00ff00)
                        embed.set_image(url=data['url'])
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send('Something went wrong.')
        else:
            embed = discord.Embed(title='Error', description='This channel is not nsfw.', color=0xFF0000)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="trap", description="Sends a random trap image. (nsfw)")
    async def trap(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=False)
        if interaction.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.waifu.pics/nsfw/trap') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        embed = discord.Embed(title='Trap',color=0x00ff00)
                        embed.set_image(url=data['url'])
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send('Something went wrong.')
        else:
            embed = discord.Embed(title='Error', description='This channel is not nsfw.', color=0xFF0000)
            await interaction.followup.send(embed=embed)     

    @app_commands.command(name="r34")
    async def r34(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        if interaction.channel.is_nsfw():
            if query:
                imgs = self.get_images(query)
                if imgs:
                    embed = discord.Embed(title='R34',color=0x00ff00)
                    embed.set_image(url=random.choice(imgs))
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send('No images found.')
            else:
                await interaction.followup.send('No query provided.')

async def setup(bot):
    bot.tree.add_command(nsfw())
