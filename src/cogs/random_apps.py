import asyncio
import io
from typing import Optional
from discord import AppCommandType, app_commands
import discord
import aiohttp
import random as aaaaa
import requests
from bs4 import BeautifulSoup
def get_facts():
    """Scrapers the website and extracts image URLs
    Returns:
        imgs [list]: List of image URLs
    """
    url = 'https://es.memedroid.com/user/view/Datos_Curiosos'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    divs = soup.find_all('div', class_='item-aux-container')
    imgs = []
    for div in divs:
        img = div.find('img')['src']
        if img.startswith('http') and img.endswith('jpeg'):
            imgs.append(img)
    return imgs

class random(app_commands.Group):
    def __init__(self):
        super().__init__()


    
    @app_commands.command(name='dog', description='Envía una imagen random de un perro')
    async def dog(self, interaction: discord.Interaction):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') 
      dogjson = await request.json()
     embed = discord.Embed(title="Doggo!", color=discord.Color.purple()) 
     embed.set_image(url=dogjson['link']) 
     await interaction.response.send_message(embed=embed) 


    @app_commands.command(name='cat', description='Envía una imagen random de un gato')
    async def cat(self, interaction: discord.Interaction):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json() 
     embed = discord.Embed(title="kitty!", color=discord.Color.purple()) 
     embed.set_image(url=catjson['link']) 
     await interaction.response.send_message(embed=embed) 

    @app_commands.command(name='fox', description='Envía una imagen random de un zorro')
    async def fox(self, interaction: discord.Interaction):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/fox')
      foxjson = await request.json() 
     embed = discord.Embed(title="Fox!", color=discord.Color.orange()) 
     embed.set_image(url=foxjson['link']) 
     await interaction.response.send_message(embed=embed) 

    @app_commands.command(name='panda', description='Envía una imagen random de un panda')
    async def panda(self, interaction: discord.Interaction):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/panda')
      pandajson = await request.json() 
     embed = discord.Embed(title="Panda!", color=discord.Color.green()) 
     embed.set_image(url=pandajson['link']) 
     await interaction.response.send_message(embed=embed) 
    
    class ViewWithButton(discord.ui.View):
        def __init__(self, *, timeout=180):
            super().__init__(timeout=timeout)
        
        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Another meme', disabled=False)
        async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            types = ["video", "img"]
            meme_type = aaaaa.choice(types)
            if meme_type == "img":

                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/memes&type=img')
                        catjson = await request.json() 
                    embed = discord.Embed(title="meme", color=discord.Color.purple()) 
                    embed.set_footer(text=f"source: {catjson['source']}")
                    embed.set_image(url=catjson['url']) 
                    await asyncio.sleep(0.4)
                    await interaction.response.send_message(embed=embed, view=self)
        
            if meme_type == "video":
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/memes&type=video')
                        catjson = await request.json() 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(catjson['url']) as af:
                            if 300 > af.status >= 200:
                                fp = io.BytesIO(await af.read())
                                file = discord.File(fp, "galactiko_com.mp4")
                                await interaction.response.send_message(file=file, view=self)
                            else:
                                await interaction.response.send_message.send('Err')
                        await session.close()

         
    @app_commands.command()
    async def meme(self, interaction: discord.Interaction):
            types = ["video", "img"]
            meme_type = aaaaa.choice(types)
            if meme_type == "img":
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/memes&type=img')
                        catjson = await request.json() 
                    embed = discord.Embed(title="meme", color=discord.Color.purple()) 
                    embed.set_footer(text=f"source: {catjson['source']}")
                    embed.set_image(url=catjson['url']) 
                    await asyncio.sleep(0.4)
                    await interaction.response.send_message(embed=embed, view=self.ViewWithButton())
            if meme_type == "video":
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/memes&type=video')
                        catjson = await request.json() 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(catjson['url']) as af:
                            if 300 > af.status >= 200:
                                fp = io.BytesIO(await af.read())
                                file = discord.File(fp, "galactiko_com.mp4")
                                await interaction.response.send_message(file=file, view=self.ViewWithButton())
                            else:
                                await interaction.response.send_message('Err')
                        await session.close()
    @app_commands.command()
    async def simpometer(self, interaction: discord.Interaction):
        percentage = (aaaaa.randint(0, 100))
        embed = discord.Embed(title="Simp O Meter", description=f"Eres {percentage}% simp", color=discord.Color.purple()) 
        embed.set_image(url='https://assets.puzzlefactory.pl/puzzle/349/392/original.jpg')
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command()
    async def fact(self, interaction: discord.Interaction):
        view = discord.ui.View() # Establish an instance of the discord.ui.View class
        style = discord.ButtonStyle.gray  # The button will be gray in color
        item = discord.ui.Button(style=style, label="Source", url="https://es.memedroid.com/user/view/Datos_Curiosos")  # Create an item to pass into the view class.
        view.add_item(item=item)  # Add that item into the view class
        embed = discord.Embed(color=discord.Color.purple()) 
        embed.set_image(url=aaaaa.choice(get_facts()))   
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    bot.tree.add_command(random())