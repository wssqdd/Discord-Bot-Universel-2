import discord
from discord.ext import commands
from discord import Streaming, app_commands
from discord.ui import Button, View
from discord import Status, Streaming
import asyncio
import random
import datetime
import json
import os
import io
from datetime import timedelta
from collections import defaultdict
import time
import re
from discord.utils import utcnow



with open("config.json", "r") as f:
    config = json.load(f)
async def get_prefix(bot, message):
    with open("config.json", "r") as f:
        data = json.load(f)
    return data["prefix"]


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Bot prêt")

salon_logs_modération = 1375733410466631780
salon_arrive = 1375731164270301226
salon_depart = 1375731164270301226
salon_staff_suggest = 1375736676814553148
salon_public_suggest = 1375736695558766652
LOG_CHANNEL_ID_BLACKLIST = 1375738730886991872
LOG_CHANNEL_ID_WARN = 1375733410466631780
role_id_staff = 1375735583690723369
NIVEAU_CHANNEL_ID = 1375856879753756833

token ="VOTRETOKEN"

@bot.command()
async def kick(ctx, membre: discord.Member = None, *, raison: str = "Aucune raison fournie"):
    salon_logs = bot.get_channel(salon_logs_modération)
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    if membre is None:
        await ctx.reply("Merci de renseigner la personne à kick du serveur")
        return
    try:
        await membre.kick(reason=raison)
        await ctx.reply(f"Le membre `{membre}` à été kick du serveur")
    except discord.Forbidden:
        await ctx.reply("Je n'ai pas la permissions de kick la personne")
    except discord.HTTPException:
        ctx.reply("Une erreur est survenu lors du kick de la personne")

    embed=discord.Embed(
        title="Kick",
        description=f"""
        > **Membre kick :** {membre}
        > **Kick par :** {ctx.author}
        > **Raison :** {raison}
        """,
        color=0xFFFFFF
    )
    await salon_logs.send(embed=embed)

@bot.command()
async def ban(ctx, membre: discord.Member = None, *, raison: str = "Aucune raison fournie"):
    salon_logs = bot.get_channel(salon_logs_modération)
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return
    embed=discord.Embed(
        title="Ban",
        description=f"""
        > **Membre ban :** {membre}
        > **Ban par :**
        > **Raison :** {raison}""",
        color=0xFFFFFF
    )
    if membre is None:
        await ctx.reply("Merci de renseigner la personne à ban du serveur")
        return
    try:
        await membre.ban(reason=raison)
        await ctx.reply(f"Le membre `{membre}` à été ban du serveur")
        await salon_logs.send(embed=embed)
    except discord.Forbidden:
        await ctx.reply("Je n'ai pas la permissions de ban la personne")
    except discord.HTTPException:
        ctx.reply("Une erreur est survenu lors du ban de la personne")

@bot.command()
async def clear(ctx, nombre: int = None):
    salon_logs = bot.get_channel(salon_logs_modération)
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    await ctx.channel.purge(limit=nombre)
    message = await ctx.send(f"`{nombre}` messages ont été supprimés")
    await asyncio.sleep(4)
    await message.delete()
    emebd=discord.Embed(
        title="Clear",
        description=f"""
        > **Nombre de messages supprimés :** {nombre}
        > **Supprimés par :** {ctx.author}""",
        color=0xFFFFFF
    )
    await salon_logs.send(embed=emebd)



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(salon_arrive)
    salon_logs = bot.get_channel(salon_logs_modération)

    role = discord.utils.get(member.guild.roles, name="Membres")
    membercount = len(member.guild.members)
    embed = discord.Embed(
        title="Bienvenue sur le serveur",
        color=0xFFFFFF,
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name=" ",value=f"""
> Nous sommes maintenant `{membercount}` sur le serveur

> N'oublie pas d'allez lire le réglement et de respecter les TOS discord""", inline=False)
    embed.set_footer(text=f"A rejoint le serveur le {(member.joined_at + datetime.timedelta(hours=2)).strftime('%d/%m/%Y à %H:%M:%S')}")
    await channel.send(embed=embed)
    await member.add_roles(role)
    embed=discord.Embed(
        title="Nouveau membre",
        description=f"""
        > **Nom :** {member}
        > **ID :** {member.id}
        > **Date de création du compte :** {member.created_at.strftime('%d/%m/%Y à %H:%M:%S')}
        > **Role attribué :** {role.mention}""",
        color=0xFFFFFF
    )
    embed.set_thumbnail(url=member.avatar.url)
    await salon_logs.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(salon_depart)
    salon_logs = bot.get_channel(salon_logs_modération)
    membercount = len(member.guild.members)
    embed = discord.Embed(
        title="À bientôt sur le serveur",
        color=0xFFFFFF,
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name=" ",value=f"""
> Nous sommes maintenant `{membercount}` sur le serveur""", inline=False)
    embed.set_footer(text=f"Avait rejoint le serveur le {(member.joined_at + datetime.timedelta(hours=2)).strftime('%d/%m/%Y à %H:%M:%S')}")
    embed.set_thumbnail(url=member.avatar.url)
    await channel.send(embed=embed)
    embed=discord.Embed(
        title="Membre parti",
        description=f"""
        > **Nom :** {member}
        > **ID :** {member.id}
        > **Date de création du compte :** {member.created_at.strftime('%d/%m/%Y à %H:%M:%S')}
        > **Role avant départ :** {member.roles[-1].mention}""",
        color=0xFFFFFF
    )
    embed.set_thumbnail(url=member.avatar.url)
    await salon_logs.send(embed=embed)

@bot.command()
async def suggest(ctx, *, suggestion: str):
    salon_staff = bot.get_channel(salon_staff_suggest)
    public_suggest = bot.get_channel(salon_public_suggest)
    embed=discord.Embed(
        title="Demande de suggestion",
        description=f"""
        > **Suggestion :** {suggestion}
        > **Suggéré par :** {ctx.author}""",
        color=0xFFFFFF
    )
    embed_public = discord.Embed(
        title="Nouvelle Suggestion",
        description=f"""

        > **Suggestion :** {suggestion}

        > Merci de réagir avec les notifications ci-dessous!""",
        color= 0xFFFFFF
    )
    embed_public.set_footer(text=f"Suggéré par {ctx.author}")
    view = View()
    btn1 = Button(label="Accepter", style=discord.ButtonStyle.green)
    btn2 = Button(label="Refuser", style=discord.ButtonStyle.red)
    view.add_item(btn1)
    view.add_item(btn2)
    async def accepter_callback(interaction: discord.Interaction):
        btn1.disabled = True
        btn2.disabled = True
        await interaction.response.edit_message(view=view)
        message = await public_suggest.send(embed=embed_public)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await interaction.followup.send("Suggestion acceptée", ephemeral=True)

    async def refuser_callback(interaction: discord.Interaction):
        btn1.disabled = True
        btn2.disabled = True
        await interaction.response.edit_message(view=view) 
        await interaction.followup.send("Suggestion refusée", ephemeral=True)

    btn1.callback = accepter_callback
    btn2.callback = refuser_callback
    await salon_staff.send(embed=embed, view=view)


def load_blacklist():
    try:
        with open("blacklist.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_blacklist(blacklist):
    with open("blacklist.json", "w") as file:
        json.dump(blacklist, file)

def make_embed(title, description):
    return discord.Embed(title=title, description=description, color=0xFF0000)

@bot.command()
async def bl(ctx, id: int):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()
        return

    blacklist = load_blacklist()

    if id in blacklist:
        await ctx.reply("L'utilisateur est déjà blacklisté.")
        return

    ban_count = 0
    for guild in bot.guilds:
        member = guild.get_member(id)
        if member:
            try:
                await guild.ban(member, reason="Utilisateur blacklisté")
                ban_count += 1
            except discord.Forbidden:
                await ctx.send(f"Pas la permission de bannir dans `{guild.name}`.")
            except discord.HTTPException:
                await ctx.send(f"Erreur HTTP lors du bannissement dans `{guild.name}`.")

    blacklist.append(id)
    save_blacklist(blacklist)

    log_channel = bot.get_channel(LOG_CHANNEL_ID_BLACKLIST)
    if log_channel:
        embed = make_embed("❌ Utilisateur blacklisté",
            f"**ID :** `{id}`\n**Par :** {ctx.author.mention}\n**Serveurs bannis :** `{ban_count}`")
        await log_channel.send(embed=embed)

    await ctx.reply(f"L'utilisateur `{id}` a été blacklisté et banni de `{ban_count}` serveur(s).")

@bot.command()
async def unbl(ctx, id: int):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()
        return

    blacklist = load_blacklist()

    if id not in blacklist:
        await ctx.reply("L'utilisateur n'est pas dans la blacklist.")
        return

    blacklist.remove(id)
    save_blacklist(blacklist)

    unban_count = 0
    for guild in bot.guilds:
        try:
            async for entry in guild.bans():
                if entry.user.id == id:
                    await guild.unban(entry.user, reason="Retiré de la blacklist")
                    unban_count += 1
        except discord.Forbidden:
            await ctx.send(f"Pas la permission de débannir dans `{guild.name}`.")
        except discord.HTTPException:
            await ctx.send(f"Erreur HTTP lors du débannissement dans `{guild.name}`.")

    log_channel = bot.get_channel(LOG_CHANNEL_ID_BLACKLIST)
    if log_channel:
        embed = make_embed("✅ Utilisateur retiré de la blacklist",
            f"**ID :** `{id}`\n**Par :** {ctx.author.mention}\n**Serveurs débannis :** `{unban_count}`")
        await log_channel.send(embed=embed)

    await ctx.reply(f"L'utilisateur `{id}` a été retiré de la blacklist et débanni de `{unban_count}` serveur(s).")

@bot.event
async def on_member_join(member):
    blacklist = load_blacklist()
    if member.id in blacklist:
        try:
            await member.ban(reason="Utilisateur blacklisté (auto-ban)")
            print(f"Utilisateur {member.id} banni automatiquement de {member.guild.name}")
        except discord.Forbidden:
            print(f"Pas la permission de bannir {member.id} dans {member.guild.name}")
        except discord.HTTPException:
            print(f"Erreur HTTP en essayant de bannir {member.id} dans {member.guild.name}")

@bot.command(name="listbl")
async def listbl(ctx):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()
        return

    blacklist = load_blacklist()

    if not blacklist:
        await ctx.reply("📭 La blacklist est vide.")
        return

    lines = []
    for user_id in blacklist:
        user = bot.get_user(user_id)
        if not user:
            try:
                user = await bot.fetch_user(user_id)
                name = f"{user.name}#{user.discriminator}"
            except discord.NotFound:
                name = "Inconnu"
            except discord.HTTPException:
                name = "Erreur API"
        else:
            name = f"{user.name}#{user.discriminator}"

        lines.append(f"- `{user_id}` ({name})")

    formatted = "\n".join(lines)
    await ctx.reply(f"📄 **Utilisateurs blacklistés ({len(blacklist)}):**\n{formatted}")

@bot.command(name="eightball", aliases=["8ball"])
async def eightball(ctx, *, question: str):
    reponses = [
        "Oui", "Non", "Peut-être", "Probablement", "Je ne sais pas", "Essaye encore", "Absolument", "Pas du tout"
    ]
    reponse = random.choice(reponses)
    await ctx.reply(f"**Question :** {question}\n**Réponse :** {reponse}")
    await ctx.message.delete()

games = {}

MAX_TRIES = 6
words = ["python", "discord", "bot", "code", "programmation", "serveur", "membre", "commande", "message"]

@bot.command()
async def hangman(ctx):
    word = random.choice(words)
    display = ["_" for _ in word]
    embed = discord.Embed(title="Jeu du Pendu", color=0xFFFFFF)
    embed.add_field(name="Mot", value=" ".join(display), inline=False)
    embed.add_field(name="Lettres devinées", value="Aucune", inline=False)
    embed.add_field(name="Essais restants", value=str(MAX_TRIES), inline=False)
    embed.set_footer(text="Tapez une lettre pour deviner.")

    msg = await ctx.send(embed=embed)

    games[ctx.channel.id] = {
        "word": word,
        "display": display,
        "guessed": [],
        "tries": MAX_TRIES,
        "message": msg
    }

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    game = games.get(message.channel.id)
    if game:
        letter = message.content.lower().strip()
        if len(letter) == 1 and letter.isalpha():
            if letter in game["guessed"]:
                await message.channel.send("Lettre déjà devinée.", delete_after=2)
            else:
                game["guessed"].append(letter)
                if letter in game["word"]:
                    for i, l in enumerate(game["word"]):
                        if l == letter:
                            game["display"][i] = letter
                    if "_" not in game["display"]:
                       
                        embed = discord.Embed(title="Jeu du Pendu - Gagné !", color=0xFFFFFF)
                        embed.add_field(name="Mot", value=" ".join(game["display"]), inline=False)
                        embed.add_field(name="Lettres devinées", value=", ".join(game["guessed"]), inline=False)
                        embed.add_field(name="Essais restants", value=str(game["tries"]), inline=False)
                        embed.set_footer(text="Bravo, vous avez gagné ! Tapez !hangman pour rejouer.")
                        await game["message"].edit(embed=embed)
                        del games[message.channel.id]
                    else:
                        embed = discord.Embed(title="Jeu du Pendu", color=0xFFFFFF)
                        embed.add_field(name="Mot", value=" ".join(game["display"]), inline=False)
                        embed.add_field(name="Lettres devinées", value=", ".join(game["guessed"]), inline=False)
                        embed.add_field(name="Essais restants", value=str(game["tries"]), inline=False)
                        embed.set_footer(text="Tapez une lettre pour deviner.")
                        await game["message"].edit(embed=embed)
                else:
                    game["tries"] -= 1
                    if game["tries"] <= 0:
                        embed = discord.Embed(title="Jeu du Pendu - Perdu !", color=0xFFFFFF)
                        embed.add_field(name="Mot", value=game["word"], inline=False)
                        embed.add_field(name="Lettres devinées", value=", ".join(game["guessed"]), inline=False)
                        embed.add_field(name="Essais restants", value="0", inline=False)
                        embed.set_footer(text="Vous avez perdu ! Tapez !hangman pour rejouer.")
                        await game["message"].edit(embed=embed)
                        del games[message.channel.id]
                    else:
                        embed = discord.Embed(title="Jeu du Pendu", color=0xFFFFFF)
                        embed.add_field(name="Mot", value=" ".join(game["display"]), inline=False)
                        embed.add_field(name="Lettres devinées", value=", ".join(game["guessed"]), inline=False)
                        embed.add_field(name="Essais restants", value=str(game["tries"]), inline=False)
                        embed.set_footer(text="Tapez une lettre pour deviner.")
                        await game["message"].edit(embed=embed)

            await message.delete()
            return

    await bot.process_commands(message)




WARN_FILE = "warn.json"



if os.path.exists(WARN_FILE):
    with open(WARN_FILE, "r", encoding="utf-8") as f:
        warns = json.load(f)
else:
    warns = {}

def save_warns():
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(warns, f, indent=4, ensure_ascii=False)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)
    reason = reason or "Aucune raison spécifiée"

    if guild_id not in warns:
        warns[guild_id] = {}

    if user_id not in warns[guild_id]:
        warns[guild_id][user_id] = []

    warns[guild_id][user_id].append(reason)
    save_warns()


    
    embed_dm = discord.Embed(title="Vous avez été warn", color=0xFFFFFF)
    embed_dm.add_field(name="> Serveur", value=f"> {ctx.guild.name}", inline=False)
    embed_dm.add_field(name="> Modérateur", value=f"> {ctx.author.mention}", inline=False)
    embed_dm.add_field(name="> Raison", value=f"> {reason}", inline=False)
    embed_dm.set_footer(text=f"Total warns : {len(warns[guild_id][user_id])}")

    try:
        await member.send(embed=embed_dm)
    except discord.Forbidden:
        await ctx.send(f"Je ne peux pas envoyer de message privé à {member.mention}.")


    log_channel = bot.get_channel(LOG_CHANNEL_ID_WARN)
    if log_channel:
        embed_log = discord.Embed(title="Warn émis", color=0xFFFFFF)
        embed_log.add_field(name="> Utilisateur warné", value=f"> {member.mention}", inline=True)
        embed_log.add_field(name="> Modérateur", value=f"> {ctx.author.mention}", inline=True)
        embed_log.add_field(name="> Raison", value=f"> {reason}", inline=False)
        embed_log.add_field(name="> Total warns", value=f"> {len(warns[guild_id][user_id])}", inline=False)
        embed_log.timestamp = ctx.message.created_at

        await log_channel.send(embed=embed_log)
    else:
        await ctx.send("Salon de logs introuvable.")

    await ctx.send(f"{member.mention} a été warn.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def unwarn(ctx, member: discord.Member, index: int = None):
    """Supprime un warn d'un membre. Si index non précisé, supprime le dernier warn."""
    guild_id = str(ctx.guild.id)
    user_id = str(member.id)

    if guild_id not in warns or user_id not in warns[guild_id] or len(warns[guild_id][user_id]) == 0:
        return await ctx.send(f"{member.mention} n'a aucun warn.")

    if index is None:
        removed_reason = warns[guild_id][user_id].pop()  
    else:
        if index < 1 or index > len(warns[guild_id][user_id]):
            return await ctx.send("Index invalide.")
        removed_reason = warns[guild_id][user_id].pop(index - 1)  


    if len(warns[guild_id][user_id]) == 0:
        del warns[guild_id][user_id]

    save_warns()

    embed_unwarn = discord.Embed(title="Warn supprimé", color=0xFFFFFF)
    embed_unwarn.add_field(name="> Utilisateur", value=f"> {member.mention}", inline=True)
    embed_unwarn.add_field(name="> Raison supprimée", value=f"> {removed_reason}", inline=False)
    await ctx.send(embed=embed_unwarn)

@bot.command()
async def listwarn(ctx, member: discord.Member = None):
    """Liste les warns d'un membre. Si aucun membre précisé, liste les warns de l'auteur."""
    guild_id = str(ctx.guild.id)

    if member is None:
        member = ctx.author

    user_id = str(member.id)

    if guild_id not in warns or user_id not in warns[guild_id] or len(warns[guild_id][user_id]) == 0:
        return await ctx.send(f"{member.mention} n'a aucun warn.")

    embed = discord.Embed(title=f"Warns de {member}", color=0xFFFFFF)
    for i, reason in enumerate(warns[guild_id][user_id], start=1):
        embed.add_field(name=f"> Warn #{i}", value=f"> {reason}", inline=False)

    await ctx.send(embed=embed)





def xp_load():
    try:
        with open("xp.json", "r") as file:
            data = json.load(file)

            if isinstance(next(iter(data.values())), int):

                data = {uid: {"xp": xp, "level": xp // 300} for uid, xp in data.items()}
                save_xp(data)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}




def save_xp(data):
    with open("xp.json", "w") as file:
        json.dump(data, file)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    xp_data = xp_load()
    user_id = str(message.author.id)

    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "level": 0}


    xp_data[user_id]["xp"] += 100


    current_xp = xp_data[user_id]["xp"]
    new_level = current_xp // 300
    previous_level = xp_data[user_id]["level"]


    if new_level > previous_level:
        xp_data[user_id]["level"] = new_level


        levelup_channel = bot.get_channel(NIVEAU_CHANNEL_ID)
        if levelup_channel:
            await levelup_channel.send(f"Merci {message.author.mention} de nous soutenir. Tu viens de passer niveau {new_level} !")


    save_xp(xp_data)

    await bot.process_commands(message)


@bot.command()
async def xp(ctx, member: discord.Member = None):
    xp_data = xp_load()
    if member is None:
        member = ctx.author

    user_id = str(member.id)

    if user_id not in xp_data:
        await ctx.send(f"{member.mention} n'a pas d'XP.")
        return

    user_xp = xp_data[user_id]["xp"]

    embed = discord.Embed(
        title=f"XP de {member.display_name}",
        color=0xFFFFFF
    )
    embed.add_field(name="XP", value=f"{user_xp}", inline=False)
    embed.set_footer(text=f"Demandé par {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.reply(embed=embed)
    await ctx.message.delete()


@bot.command()
async def level(ctx, member: discord.Member = None):
    xp_data = xp_load()
    if member is None:
        member = ctx.author

    user_id = str(member.id)

    if user_id not in xp_data:
        await ctx.send(f"{member.mention} n'a pas de niveau.")
        return

    user_level = xp_data[user_id]["level"]

    embed = discord.Embed(
        title=f"Niveau de {member.display_name}",
        color=0xFFFFFF
    )
    embed.add_field(name="Niveau", value=f"{user_level}", inline=False)
    embed.set_footer(text=f"Demandé par {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.reply(embed=embed)
    await ctx.message.delete()


@bot.command()
async def leaderboard_xp(ctx, top: int = 10):
    xp_data = xp_load()
    sorted_xp = sorted(xp_data.items(), key=lambda item: item[1]["xp"], reverse=True)
    top_users = sorted_xp[:top]

    embed = discord.Embed(
        title=f"Leaderboard XP - Top {top}",
        color=0xFFFFFF
    )

    for i, (user_id, data) in enumerate(top_users, start=1):
        member = ctx.guild.get_member(int(user_id))
        name = member.display_name if member else f"Utilisateur inconnu ({user_id})"
        embed.add_field(
            name=f"{i}. {name}",
            value=f"**XP :** {data['xp']}\n**Niveau :** {data['level']}",
            inline=False
        )

    embed.set_footer(
        text=f"Demandé par {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )

    await ctx.reply(embed=embed)
    await ctx.message.delete()


@bot.command()
async def leaderboard_level(ctx, top: int = 10):
    xp_data = xp_load()
    sorted_level = sorted(xp_data.items(), key=lambda item: item[1]["level"], reverse=True)
    top_users = sorted_level[:top]

    embed = discord.Embed(
        title=f"Leaderboard Niveau - Top {top}",
        color=0xFFFFFF
    )

    for i, (user_id, data) in enumerate(top_users, start=1):
        member = ctx.guild.get_member(int(user_id))
        name = member.display_name if member else f"Utilisateur inconnu ({user_id})"
        embed.add_field(
            name=f"{i}. {name}",
            value=f"**Niveau :** {data['level']}\n**XP :** {data['xp']}",
            inline=False
        )

    embed.set_footer(
        text=f"Demandé par {ctx.author.display_name}",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )

    await ctx.reply(embed=embed)
    await ctx.message.delete()




@bot.command()
async def givepoint(ctx, member: discord.Member, points: int):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()
        return
    xp = xp_load()
    user_id = str(member.id)
    if user_id not in xp:
        xp[user_id] = 0
    xp[user_id] += points
    save_xp(xp)
    aze = await ctx.reply(f"{points} points ont été ajoutés à {member.mention}.")
    await ctx.message.delete()
    await asyncio.sleep(4)
    await aze.delete()

@bot.command()
async def removepoint(ctx, member: discord.Member, points: int):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.reply("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await msg.delete()
        return
    xp = xp_load()
    user_id = str(member.id)
    if user_id not in xp:
        xp[user_id] = 0
    xp[user_id] -= points
    save_xp(xp)
    aze = await ctx.reply(f"{points} points ont été enlevés à {member.mention}.")
    await ctx.message.delete()
    await asyncio.sleep(4)
    await aze.delete()









fiche_file = "fiche.json"


if os.path.exists(fiche_file):
    with open(fiche_file, "r", encoding="utf-8") as f:
        fiche_data = json.load(f)
else:
    fiche_data = {"fiches": []}


def create_embed(fiches, index):
    fiche = fiches[index]
    embed = discord.Embed(
        title=fiche["nom"],
        description=fiche["description"],
        color=0xFFFFFF
    )
    embed.set_image(url=fiche["image"])
    embed.add_field(name="Lien", value=fiche["lien"], inline=False)
    embed.set_footer(text=f"Fiche {index + 1} / {len(fiches)} | Utilisez les flèches pour naviguer")
    return embed


@bot.command(name="fiche")
async def fiche(ctx):
    fiches_list = fiche_data["fiches"]
    if not fiches_list:
        await ctx.send("Aucune fiche disponible.")
        return

    index = 0
    view = discord.ui.View()

    async def update_embed(interaction, delta):
        nonlocal index
        index = (index + delta) % len(fiches_list)
        await interaction.response.edit_message(embed=create_embed(fiches_list, index), view=view)

    back_button = discord.ui.Button(emoji="<:left:1376568966222319697>", style=discord.ButtonStyle.gray)
    forward_button = discord.ui.Button(emoji="<:right:1376568984786440302>", style=discord.ButtonStyle.gray)


    async def back_callback(interaction: discord.Interaction):
        await update_embed(interaction, -1)

    async def forward_callback(interaction: discord.Interaction):
        await update_embed(interaction, 1)

    back_button.callback = back_callback
    forward_button.callback = forward_callback

    view.add_item(back_button)
    view.add_item(forward_button)

    await ctx.reply(embed=create_embed(fiches_list, index), view=view)
    await ctx.message.delete()
    
@bot.command(name="addfiche")
async def addfiche(ctx, nom: str, description: str, image: str, lien: str):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.send("Vous n'avez pas la permission d'ajouter une fiche.")
        await asyncio.sleep(4)
        await ctx.message.delete()
        return
        
    nouvelle_fiche = {
        "nom": nom,
        "description": description,
        "image": image,
        "lien": lien
    }


    fiche_data["fiches"].append(nouvelle_fiche)
    

    with open(fiche_file, "w", encoding="utf-8") as f:
        json.dump(fiche_data, f, ensure_ascii=False, indent=4)

    msg = await ctx.send(f"Fiche ajoutée : **{nom}**")
    await asyncio.sleep(4)
    await msg.delete()




@bot.command()
async def setup_ticket(ctx, catégorie1: str, catégorie2: str, catégorie3: str):
    if not ctx.author.guild_permissions.administrator:
        msg = await ctx.send("Vous n'avez pas la permission")
        await asyncio.sleep(4)
        await ctx.message.delete()
        return
    staff = discord.utils.get(ctx.guild.roles, id=role_id_staff)
    embed=discord.Embed(
        title="Ticket",
        description=f"""
        > Voici les catégories disponible:
        >  - {catégorie1}
        >  - {catégorie2}
        >  - {catégorie3}""",
        color=0xFFFFFF
    )
    catégorie1_btn = discord.ui.Button(label=catégorie1, style=discord.ButtonStyle.secondary)
    catégorie2_btn = discord.ui.Button(label=catégorie2, style=discord.ButtonStyle.secondary)
    catégorie3_btn = discord.ui.Button(label=catégorie3, style=discord.ButtonStyle.secondary)
    view = discord.ui.View(timeout=None)
    view.add_item(catégorie1_btn)
    view.add_item(catégorie2_btn)
    view.add_item(catégorie3_btn)
    logs = discord.utils.get(ctx.guild.text_channels, name="logs")
    if logs is None:
        logs = await ctx.guild.create_text_channel("logs")
        await logs.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
        await logs.set_permissions(staff, read_messages=True, send_messages=True)
        await logs.send("Logs Initialisés")
    embed_ouverture = discord.Embed(
        title="🎫 Nouveau Ticket",
        description="""
> Veuillez expliquer votre problème et un membre du staff vous aidera rapidement.
> 📋 Informations
> • Décrivez votre problème en détail
> • Un staff vous répondra rapidement
> • Utilisez les boutons ci-dessous pour fermer""",
        color=0xFFFFFF
    )
    view_close = discord.ui.View(timeout=None)
    btn_close = discord.ui.Button(label="Fermer le ticket", style=discord.ButtonStyle.red)
    async def close_callback(interaction: discord.Interaction):
        async def confirm(interaction_confirm: discord.Interaction):

            lines = []
            async for msg in interaction_confirm.channel.history(limit=None, oldest_first=True):
                timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M")
                author = msg.author.display_name
                content = msg.content
                lines.append(f"[{timestamp}] {author}: {content}")

            transcript_text = "\n".join(lines)
            file = io.StringIO(transcript_text)
            file.seek(0)

            transcript_file = discord.File(fp=file, filename=f"transcript-{interaction_confirm.channel.name}.txt")


            embed_close = discord.Embed(
                title="Ticket Fermé",
                description=f"""
        > **Ticket Fermé par :** {interaction_confirm.user.mention}
        > **ID :** {interaction_confirm.user.id}""",
                color=discord.Color.red()
            )


            await logs.send(embed=embed_close, file=transcript_file)


            await interaction_confirm.response.send_message("Ticket fermé, fermeture en cours...", ephemeral=True)


            await interaction_confirm.channel.delete()
            view_close_2.stop()

        async def cancel(interaction_cancel: discord.Interaction):
            await interaction_cancel.response.send_message("Fermeture annulée.", ephemeral=True)
            view_close_2.stop()

        btn_confirm = discord.ui.Button(label="Oui", style=discord.ButtonStyle.danger)
        btn_cancel = discord.ui.Button(label="Non", style=discord.ButtonStyle.secondary)
        view_close_2 = discord.ui.View()
        btn_confirm.callback = confirm
        btn_cancel.callback = cancel

        view_close_2.add_item(btn_confirm)
        view_close_2.add_item(btn_cancel)

        await interaction.response.send_message(
            "Êtes-vous sûr·e de vouloir fermer ce ticket ?", 
            view=view_close_2, 
            ephemeral=True
        )
    btn_close.callback = close_callback
    view_close.add_item(btn_close)
    category = discord.utils.get(ctx.guild.categories, name="Tickets")
    if category is None:
        category = await ctx.guild.create_category("Tickets")
    async def cat1_calklback(interaction: discord.Interaction):
        chnl = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user}", category=category)
        await interaction.response.send_message(f"Ticket créé {chnl.mention}", ephemeral=True)
        await chnl.send(embed=embed_ouverture, view=view_close)
        embed_logs_open = discord.Embed(
            title="Ticket Ouvert",
            description=f"""
            > **Ticket Ouvert par :** {interaction.user.mention}
            > **ID :** {interaction.user.id}
            > **Catégorie :** {catégorie1}""",
            color=discord.Color.green()
        )
        await logs.send(embed=embed_logs_open)
        
        a = await chnl.send(f"{interaction.user.mention} {staff.mention}")
        await a.delete()
        await chnl.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await chnl.set_permissions(staff, read_messages=True, send_messages=True)
        await chnl.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    async def cat2_calklback(interaction: discord.Interaction):
        chnl = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user}", category=category)
        await interaction.response.send_message(f"Ticket créé {chnl.mention}", ephemeral=True)
        await chnl.send(embed=embed_ouverture, view=view_close)
        embed_logs_open = discord.Embed(
            title="Ticket Ouvert",
            description=f"""
            > **Ticket Ouvert par :** {interaction.user.mention}
            > **ID :** {interaction.user.id}
            > **Catégorie :** {catégorie2}""",
            color=discord.Color.green()
        )
        await logs.send(embed=embed_logs_open)
        a = await chnl.send(f"{interaction.user.mention} {staff.mention}")
        await a.delete()
        await chnl.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await chnl.set_permissions(staff, read_messages=True, send_messages=True)
        await chnl.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    async def cat3_calklback(interaction: discord.Interaction):
        chnl = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user}", category=category)
        await interaction.response.send_message(f"Ticket créé {chnl.mention}", ephemeral=True)
        await chnl.send(embed=embed_ouverture, view=view_close)
        embed_logs_open = discord.Embed(
            title="Ticket Ouvert",
            description=f"""
            > **Ticket Ouvert par :** {interaction.user.mention}
            > **ID :** {interaction.user.id}
            > **Catégorie :** {catégorie3}""",
            color=discord.Color.green()
        )
        await logs.send(embed=embed_logs_open)
        a = await chnl.send(f"{interaction.user.mention} {staff.mention}")
        await a.delete()
        await chnl.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await chnl.set_permissions(staff, read_messages=True, send_messages=True)
        await chnl.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    catégorie1_btn.callback = cat1_calklback
    catégorie2_btn.callback = cat2_calklback
    catégorie3_btn.callback = cat3_calklback
    
    await ctx.send(embed=embed, view=view)
        
        
@bot.command()
async def antilien(ctx, state: str):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    state = state.lower()
    if state not in ["on", "off"]:
        return await ctx.reply("Utilisez `on` ou `off`.")

    with open("config.json", "r") as f:
        config = json.load(f)

    current = config.get("antilien", False)
    new = (state == "on")

    if current == new:
        return await ctx.reply(f"ℹL'antilien est déjà {'activé' if new else 'désactivé'}.")

    config["antilien"] = new
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.reply(f"L'antilien a bien été {'activé' if new else 'désactivé'}.")



@bot.command()
async def antispam(ctx, mode: str = None, level: int = 1):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    mode = mode.lower() if mode else None
    if mode not in ["on", "off"]:
        return await ctx.reply("Utilisez `.antispam on <niveau>` ou `.antispam off`.")

    with open("config.json", "r") as f:
        config = json.load(f)

    if mode == "on":
        if not (1 <= level <= 3):
            return await ctx.reply("Le niveau doit être entre 1 et 3.")
        config["antispam"] = level
        await ctx.reply(f"Antispam activé (niveau {level}).")
    else:
        config["antispam"] = 0
        await ctx.reply("Antispam désactivé.")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


user_message_times = defaultdict(list)
user_warnings = defaultdict(int)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    level = config.get("antispam", 0)
    if level:
        settings = {
            1: {"interval": 10, "max_messages": 5},
            2: {"interval": 7, "max_messages": 4},
            3: {"interval": 5, "max_messages": 3}
        }.get(level, {"interval": 10, "max_messages": 5})

        now = time.time()
        user_id = message.author.id
        user_message_times[user_id].append(now)
        user_message_times[user_id] = [t for t in user_message_times[user_id] if now - t < settings["interval"]]

        if len(user_message_times[user_id]) > settings["max_messages"]:
            user_warnings[user_id] += 1
            await message.delete()

            if user_warnings[user_id] >= 3:
                try:
                    duration = timedelta(hours=1)
                    await message.author.timeout(duration, reason="Antispam : 3 avertissements")

                    await message.channel.send(
                        f"{message.author.mention} Tu as été mis en timeout pendant 1 heure pour spam.",
                        delete_after=5
                    )
                except Exception as e:
                    print(f"[ERREUR TIMEOUT] : {e}")
            else:
                await message.channel.send(
                    f"{message.author.mention} Merci de ne pas spammer ! (Avertissement {user_warnings[user_id]}/3)",
                    delete_after=5
                )
            return

    await bot.process_commands(message)




@bot.command()
async def antibot(ctx, state: str):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    state = state.lower()
    if state not in ["on", "off"]:
        return await ctx.reply("Utilisez `on` ou `off`.")

    with open("config.json", "r") as f:
        config = json.load(f)

    current = config.get("antibot", False)
    if (state == "on" and current) or (state == "off" and not current):
        return await ctx.reply(f"L'antibot est déjà {'activé' if current else 'désactivé'}.")

    config["antibot"] = (state == "on")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.reply(f"L'antibot est maintenant {'activé' if state == 'on' else 'désactivé'}.")


@bot.event
async def on_member_join(member):
    with open("config.json", "r") as f:
        config = json.load(f)

    if config.get("antibot", False):
        if member.bot:
            try:
                await member.kick(reason="Antibot activé : tentative d'ajout d'un bot.")
                channel = discord.utils.get(member.guild.text_channels, name="📁-·log-join-leave")  
                if channel:
                    embed = make_embed(
                    "🛑 Bot expulsé automatiquement",
                    f"Le bot {member.mention} a été expulsé automatiquement en raison de la protection antibot activée."
                )
                await channel.send(embed=embed)
            except Exception as e:
                print(f"[ERREUR ANTIBOT] : {e}")


@bot.command()
async def antiinvitation(ctx, state: str):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    state = state.lower()
    if state not in ["on", "off"]:
        return await ctx.reply("Utilisez `on` ou `off`.")

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    config["antiinvitation"] = (state == "on")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    await ctx.reply(f"L'antiinvitation est maintenant {'activé' if state == 'on' else 'désactivé'}.")

    if state == "on":

        try:
            invites = await ctx.guild.invites()
            for invite in invites:
                await invite.delete()
        except Exception as e:
            print(f"[Erreur suppression d'invites] : {e}")


        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    create_instant_invite=False
                )
            except Exception as e:
                print(f"[Erreur permissions sur {channel.name}] : {e}")

    elif state == "off":

        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(
                    ctx.guild.default_role,
                    create_instant_invite=None 
                )
            except Exception as e:
                print(f"[Erreur réactivation sur {channel.name}] : {e}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return  


    if message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return


    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    if config.get("antilien", False):
        url_pattern = re.compile(r'https?://\S+')
        links = url_pattern.findall(message.content)
        if links:
            non_tenor_links = [link for link in links if "tenor.com" not in link.lower()]
            if non_tenor_links:
                try:
                    await message.delete()
                    warning = await message.channel.send(
                        f"{message.author.mention}, les liens sont interdits"
                    )
                    await asyncio.sleep(5)
                    await warning.delete()
                except discord.Forbidden:
                    print("Je n'ai pas la permission de supprimer les messages.")
                except Exception as e:
                    print(f"Erreur dans l'antilien : {e}")
                return
    if not message.author.guild_permissions.administrator:
        majuscule_level = config.get("antimajuscule", 0)
        if majuscule_level and len(message.content) >= 5:

            thresholds = {
                1: 0.9, 
                2: 0.75,
                3: 0.6   
            }

            threshold = thresholds.get(majuscule_level, 0.9)
            letters = [c for c in message.content if c.isalpha()]
            if letters:
                upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
                if upper_ratio >= threshold:
                    try:
                        await message.delete()
                        warn = await message.channel.send(
                            f"{message.author.mention}, merci d'éviter d'écrire en majuscules.",
                            delete_after=5
                        )
                    except Exception as e:
                        print(f"[ERREUR ANTIMAJUSCULE] : {e}")
                    return
    await bot.process_commands(message)

@bot.command()
async def prefix(ctx, prefix:str):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return
    config["prefix"]=prefix
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    await ctx.send(f"Le préfixe a été changé en `{prefix}`")

@bot.command()
async def vid(ctx, lien:str):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
    msg = await ctx.reply(f"**J'ai sortit une nouvelle vidéo allez la voir ici : [Cliqué ici]({lien})** ||@everyone||")
    await msg.add_reaction("🔥")
    await ctx.message.delete()

@bot.command()
async def antimajuscule(ctx, mode: str = None, level: int = 1):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    mode = mode.lower() if mode else None
    if mode not in ["on", "off"]:
        return await ctx.reply("Utilisez `.antimajuscule on <niveau>` ou `.antimajuscule off`.")

    with open("config.json", "r") as f:
        config = json.load(f)

    if mode == "on":
        if not (1 <= level <= 3):
            return await ctx.reply("Le niveau doit être entre 1 et 3.")
        config["antimajuscule"] = level
        await ctx.reply(f"Antimajuscule activé (niveau {level}).")
    else:
        config["antimajuscule"] = 0
        await ctx.reply("Antimajuscule désactivé.")

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


@bot.command()
async def mute(ctx, author: discord.Member, temps: int):
    if not ctx.author.guild_permissions.administrator:
        a = await ctx.channel.send("Vous n'avez pas la permission d'effectuer cette commande")
        await asyncio.sleep(2)
        await ctx.message.delete()
        await a.delete()
        return

    until = utcnow() + timedelta(hours=temps)

    try:
        await author.timeout(until, reason=f"Mute par {ctx.author} pendant {temps} heure(s)")
        msg = await ctx.reply(f"{author.mention} a été mute pendant {temps} heure(s).")
        await asyncio.sleep(4)
        await msg.delete()
        await ctx.message.delete()
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions nécessaires pour mute cet utilisateur (rôle trop élevé ou permission manquante).")
    except Exception as e:
        await ctx.send(f"Erreur lors du mute : {e}")



@bot.command()
async def help(ctx):
    # Récupérer dynamiquement le préfixe actuel
    with open("config.json", "r") as f:
        data = json.load(f)
    prefix = data["prefix"]

    embed = discord.Embed(
        title="Listes des commandes disponibles",
        description="Voici quelques commandes que vous pouvez utiliser avec ce bot :",
        color=config.get("color_embed")
    )

    embed.add_field(name=" ", value=f"""
**`{prefix}fiche`**
> Permet de voir les fiches disponibles

**`{prefix}level`**
> Permet de voir votre niveau

**`{prefix}xp`**
> Permet de voir votre xp

**`{prefix}leaderboard_xp`**
> Permet de voir le leaderboard xp

**`{prefix}leaderboard_level`**
> Permet de voir le leaderboard niveau

**`{prefix}suggest`**
> Permet de faire une suggestion

**`{prefix}hangman`**
> Permet de jouer au pendu

**`{prefix}8ball`**
> Permet de poser une question au bot

**`{prefix}help_admin`**
> Permet de voir les commandes de modération

""", inline=False)

    embed.set_footer(text=f"Préfix actuel: {prefix} | Demandé par {ctx.author}")

    await ctx.reply(embed=embed)
    await ctx.message.delete()

@bot.command()
async def help_admin(ctx):
    # Récupérer dynamiquement le préfixe actuel
    with open("config.json", "r") as f:
        data = json.load(f)
    prefix = data["prefix"]

    embed = discord.Embed(
        title="Listes des commandes de modération",
        description="Voici quelques commandes que vous pouvez utiliser avec ce bot :",
        color=config.get("color_embed")
    )

    embed.add_field(name=" ", value=f"""
**`{prefix}antibot`**
> Permet d'activer ou de désactiver l'antibot

**`{prefix}antiinvitation`**
> Permet d'activer ou de désactiver l'antiinvitation

**`{prefix}antilien`**
> Permet d'activer ou de désactiver l'antilien

**`{prefix}antimajuscule`**
> Permet d'activer ou de désactiver l'antimajuscule

**`{prefix}antispam`**
> Permet d'activer ou de désactiver l'antispam

**`{prefix}bl`**
> Permet de blacklist un membre

**`{prefix}unbl`**
> Permet de unblacklist un membre

**`{prefix}listbl`**
> Permet de voir la liste des membres blacklist

**`{prefix}addfiche`**
> Permet d'ajouter une fiche

**`{prefix}setup_ticket`**
> Permet de setup le système de ticket

**`{prefix}prefix`**
> Permet de changer le préfix

**`{prefix}vid`**
> Permet de sortir une vidéo

**`{prefix}mute`**
> Permet de mute un membre

**`{prefix}unwarn`**
> Permet de unwarn un membre

**`{prefix}listwarn`**
> Permet de voir la liste des warns d'un membre

**`{prefix}givepoint`**
> Permet de donner des points à un membre

**`{prefix}removepoint`**
> Permet de retirer des points à un membre

""", inline=False)

    embed.set_footer(text=f"Préfix actuel: {prefix} | Demandé par {ctx.author}")

    await ctx.reply(embed=embed)
    await ctx.message.delete()



bot.run(token)
