from discord.ext import commands
from discord import Message
import discord
import aiohttp

class inter(commands.Cog):  # All cogs must inherit from commands.Cog
    """A simple, basic cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='hug')
    async def hug(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.message.mentions[0]
        if member == ctx.message.author:
            await ctx.send("No puedes abrazarte a ti mismo")
            return
        else:
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://some-random-api.ml/animu/hug')
                hugjson = await request.json() 
            embed = discord.Embed(title=f"{ctx.author.mention} abrazó a {member.mention}", color=discord.Color.green()) 
            embed.set_image(url=hugjson['link']) 
            await ctx.send(embed=embed)

    @commands.command(name='pat')
    async def pat(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.message.mentions[0]
        if member == ctx.message.author:
            await ctx.send("No puedes acariciarte a ti mismo")
            return
        else:
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://some-random-api.ml/animu/pat')
                patjson = await request.json() 
            embed = discord.Embed(title=f"{ctx.author.mention} acarició a {member.mention}", color=discord.Color.green()) 
            embed.set_image(url=patjson['link']) 
            await ctx.send(embed=embed) 

    @commands.command(name='wink')
    async def wink(self, ctx: commands.Context):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/animu/wink')
      winkjson = await request.json() 
     embed = discord.Embed(title=f"{ctx.author.mention} guiñó el ojo", color=discord.Color.green()) 
     embed.set_image(url=winkjson['link']) 
     await ctx.send(embed=embed) 

async def setup(bot):
    await bot.add_cog(inter(bot))