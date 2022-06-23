from discord import app_commands
import discord
import aiohttp

class act(app_commands.Group):  
    def __init__(self):
        super().__init__()
    
    @app_commands.command(name='hug')
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/hug')
            hugjson = await request.json() 
        embed = discord.Embed(title=f"{interaction.user.name} abrazó a {member.name}", color=discord.Color.green()) 
        embed.set_image(url=hugjson['link']) 
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='pat')
    async def pat(self, interaction: discord.Interaction, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/pat')
            patjson = await request.json() 
        embed = discord.Embed(title=f"{interaction.user.name} acarició a {member.name}", color=discord.Color.green()) 
        embed.set_image(url=patjson['link']) 
        await interaction.response.send_message(embed=embed) 

    @app_commands.command(name='wink')
    async def wink(self, interaction: discord.Interaction):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/animu/wink')
      winkjson = await request.json() 
     embed = discord.Embed(title=f"{interaction.user.name} guiñó el ojo", color=discord.Color.green()) 
     embed.set_image(url=winkjson['link']) 
     await interaction.response.send_message(embed=embed) 

async def setup(bot):
    bot.tree.add_command(act())