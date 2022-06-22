import json
import re
import discord
from typing import Optional
from discord import app_commands


class mod(app_commands.Group):
    def __init__(self):
        super().__init__()


    @app_commands.command(name="muted-role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def muted_role(self, interaction: discord.Interaction, role: discord.Role):
        with open("mutedrole.json", "r") as f:
            prefixes = json.load(f)
            prefixes[str(interaction.guild.id)] = role.id
        with open("mutedrole.json", "w") as f:
            json.dump(prefixes, f, indent=4)
            await interaction.response.send_message(f"Muted role has been seted to:{role.mention}")
      
    @app_commands.command(name="mute", description="Silencia al usuario especificado")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason:Optional[str] = None, time:Optional[int] = None):
        with open("mutedrole.json", "r") as f: #Abre el archivo donde se encuentra la id del rol para el Muted
         mrole = json.load(f) #Carga el archivo
         eole = mrole.get(str(interaction.guild.id)) #Carga el Archivo
        mutedRole = discord.utils.get(interaction.guild.roles, id=eole) #Obtiene el rol
        if not mutedRole:
            await interaction.response.send_message("No hay un rol de muted establecido, usa `/mod muted-role` para establecer uno ", ephemeral=True)
            return
        if mutedRole in member.roles:
            await interaction.response.send_message("El usuario ya está silenciado", ephemeral=True)
            return
        else:
            embed = discord.Embed(title="Shhh", description=f"{member.mention} fue silenciado ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            await member.add_roles(mutedRole, reason=reason)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def adsjadhjas(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        with open("mutedrole.json", "r") as f: #Abre el archivo donde se encuentra la id del rol para el Muted
         mrole = json.load(f) #Carga el .json
         eole = mrole.get(str(interaction.guild.id)) #Obtiene el id con la id del server
        mutedRole = discord.utils.get(interaction.guild.roles, id=eole) #Busca el rol por ID
        if not mutedRole:
            await interaction.response.send_message("No hay un rol de muted establecido, usa `/mod muted-role` para establecer uno ", ephemeral=True)
            return
        if mutedRole not in member.roles:
            await interaction.response.send_message("El usuario no esta silenciado", ephemeral=True)
            return
        else:
            embed = discord.Embed(title="Unmute", description=f"{member.mention} fue desilienciado ", colour=discord.Colour.light_gray()) #Crea el embed
            embed.add_field(name="reason:", value=reason, inline=False) #Envía el embed
            await member.remove_roles(mutedRole) #Quita el mute
            await interaction.response.send_message(embed=embed) #Envía el embed


    @app_commands.command(name='ban', description='banea al usuario especificado')
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, member : discord.User, reason: Optional[str] = None):
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message("No puedes banear a un usuario con un rol mayor o igual que tu rol")
            return
        else:
            try:
                await member.ban(reason=reason)
            except Exception as e:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)
                return
            await interaction.response.send_message(f"{member.mention} fue baneado")
    

    @app_commands.command(name='kick', description='Expulsa al usuario especificado')
    @app_commands.checks.has_permissions(kick_members = True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if interaction.user.top_role <= member.top_role:
            await interaction.response.send_message("No puedes expulsar a un usuario con unarol mayor o igual que tu", ephemeral=True)
        else:
            try:
                await member.kick(reason=f"{interaction.user} kicked {member} with reason:{reason}")
            except Exception as e:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)
                return
            embed = discord.Embed(title="kicked", description=f"{member.mention} has been kicked", colour=discord.Colour.light_gray())
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(mod())