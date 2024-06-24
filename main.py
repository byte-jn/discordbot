import discord
from discord.ext import commands, tasks
import os
import requests
import json
import asyncio
import random
from datetime import datetime
from server import Live
from Hello import random_language
from Hallo import random_greeting, random_greeting_evening, random_greeting_morning, random_greeting_night
from names import names
from youtubeapi import youtubeapi, youtubeapilong, youtubeapimemeslong, youtubeapisearch, youtubeapimemes, youtubeshortapi, youtubeshortsapimemes, ytapi, randomyoutubeapi

# Definiere Konstanten aus den Umgebungsvariablen
DAILY_CLEARING_CHANNEL_ID = os.getenv('DAILY_CLEARING_CHANNEL_ID')  # Kanal-ID für tägliches Löschen
YOUR_SERVER_ID = os.getenv('YOUR_SERVER_ID')  # Server-ID
YOUR_CHANNEL_ID = os.getenv('YOUR_CHANNEL_ID')  # Kanal-ID
YOUR_DISCORD_BOT_TOKEN = os.getenv('YOUR_DISCORD_BOT_TOKEN')  # Discord-Bot-Token

# Erstelle Intents für den Bot, um bestimmte Ereignisse zu behandeln
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='', intents=intents)

# Initialisiere die Startzeit und einige globale Variablen
start_time = datetime.now()
daily_video_online = {}
happycrismas = {}

@tasks.loop(minutes=5)
async def update_time():
    # Lösche die Konsole
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Berechne die verstrichene Zeit und aktualisiere den Bot-Status
    elapsed_time = datetime.now() - start_time
    elapsed_minutes = int(elapsed_time.total_seconds() / 60)
    activity = discord.Game(name=f"seit {round(elapsed_minutes/60)}h", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    
    # Aktuelle Uhrzeit und Datum
    current_hour = datetime.now().hour + 1
    current_minute = datetime.now().minute
    current_second = datetime.now().second
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Guild-ID für tägliches Video-Update
    guild_id = YOUR_SERVER_ID
    if guild_id not in daily_video_online:
        daily_video_online[guild_id] = False

    # Bedingte Aufgaben basierend auf der Uhrzeit
    if current_hour == 18:
        if not daily_video_online[guild_id]:
            await send_daily_video(guild_id, 'daily')
    elif current_hour == 20:
        if not daily_video_online[guild_id]:
            await send_daily_meme(guild_id)
    elif current_month == 12 and current_day == 24 and current_hour == 12:
        if not daily_video_online[guild_id]:
            await send_christmas_greeting(guild_id)
    elif current_month == 12 and current_day == 31 and current_hour == 23 and 55 >= current_minute >= 50:
        if not daily_video_online[guild_id]:
            bot.loop.create_task(countdown())
            daily_video_online[guild_id] = True
    else:
        daily_video_online[guild_id] = False
    print(f"Aktualisierte Zeit: {elapsed_minutes}min ( {current_day}.{current_month}.{current_year} )( {current_hour}:{current_minute}:{current_second} ) ( Daily Video {daily_video_online[guild_id]} ) Nächste Aktualisierung in 5 min ")

@bot.event
async def on_ready():
    # Logge, dass der Bot bereit ist und starte die Zeitaktualisierung
    log_event("Bot is ready!")
    update_time.start()

@bot.event
async def on_member_join(member):
    # Begrüße neue Mitglieder
    guild_id = YOUR_SERVER_ID
    if guild_id:
        await send_welcome_message(member, guild_id)

@bot.command()
async def countdownxyz(ctx):
    # Starte den Countdown
    bot.loop.create_task(countdown())

async def countdown():
    # Countdown-Prozess bis zum Jahreswechsel
    current_year = datetime.utcnow().year
    guild_id = YOUR_SERVER_ID
    channel_id = YOUR_CHANNEL_ID
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            await channel.send(f"Nicht mehr lang bis {current_year + 1}")
            await countdown_process(channel, current_year)

@bot.command()
async def displaylog(ctx):
    # Zeige den Inhalt der Logdatei
    await display_file_content(ctx, "log.txt")

@bot.command()
async def displaymemberlog(ctx):
    # Zeige den Inhalt der Mitglieder-Logdatei
    await display_file_content(ctx, "memberlog.txt")

# YouTube-Befehle
@bot.command()
async def youtube(ctx):
    await handle_youtube_command(ctx, youtubeapi)

@bot.command()
async def randomyoutube(ctx):
    await handle_youtube_command(ctx, randomyoutubeapi)

@bot.command()
async def yt(ctx):
    await handle_youtube_command(ctx, ytapi)

@bot.command()
async def longyoutube(ctx):
    await handle_youtube_command(ctx, youtubeapilong)

@bot.command()
async def shortyoutube(ctx):
    await handle_youtube_command(ctx, youtubeshortapi)

@bot.command()
async def youtubememe(ctx):
    await handle_youtube_command(ctx, youtubeapimemes, 1)

@bot.command()
async def longyoutubememe(ctx):
    await handle_youtube_command(ctx, youtubeapimemeslong, 1)

@bot.command()
async def shortyoutubememe(ctx):
    await handle_youtube_command(ctx, youtubeshortsapimemes, 1)

@bot.command()
async def youtubememes(ctx, number=None):
    await handle_youtube_command(ctx, youtubeapimemes, number, True)

@bot.command()
async def longyoutubememes(ctx, number=None):
    await handle_youtube_command(ctx, youtubeapimemeslong, number, True)

@bot.command()
async def shortyoutubememes(ctx, number=None):
    await handle_youtube_command(ctx, youtubeshortsapimemes, number, True)

@bot.command()
async def search(ctx, text):
    await handle_youtube_command(ctx, youtubeapisearch, text)

# Spaß- und Begrüßungsbefehle
@bot.command()
async def toilette(ctx):
    await ctx.send("https://youtu.be/3DpjtBWYifg?si=2NnvHDZky2meF5dH")

@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme")
    json_data = json.loads(response.text)
    await ctx.send(json_data.get("url"))

# Begrüßungsbefehle
@bot.command()
async def hallo(ctx):
    await send_greeting(ctx)

@bot.command()
async def hey(ctx):
    await send_greeting(ctx)

@bot.command()
async def na(ctx):
    await send_greeting(ctx, night=True)

@bot.command()
async def moin(ctx):
    await send_greeting(ctx)

@bot.command()
async def hi(ctx):
    await send_greeting(ctx)

@bot.command()
async def write(ctx, text):
    await ctx.send(text)

# Begrüßung in verschiedenen Sprachen
@bot.command()
async def hello(ctx):
    await ctx.send(random_language())

@bot.command()
async def sus(ctx):
    await ctx.send("https://youtu.be/keyRM3h_7tk?si=eIIx3UGRqVKThGsi")

@bot.command()
async def imposter(ctx):
    await ctx.send("https://youtu.be/RMyFf73Stoc?si=P_H3VNaiENCyBmUL")

async def clear_channel(ctx, limit=5):
    channel = ctx.message.channel
    if not channel:
        print("Invalid channel ID provided.")
    else:
        while True:
            await clear_messages(channel, limit)
            channel = ctx.message.channel
            if not channel.last_message:
                break
            await asyncio.sleep(10)
    print(f"All cleared in channel {channel.name}")

async def clear_messages(channel, limit):
    try:
        async for message in channel.history(limit=limit):
            await message.delete()
        print(f"Channel ({channel}) got a little bit cleared.")
    except discord.Forbidden:
        print("Bot does not have the necessary permissions to delete messages.")
    except discord.HTTPException as e:
        if e.status == 429:
            retry_after = e.retry_after
            print(f"Rate limited. Retrying in {retry_after} seconds.")
            await asyncio.sleep(retry_after)
            await clear_messages(channel, limit)
        else:
            print(f"An error occurred while deleting messages: {e}")

# Hilfsfunktionen
def log_event(message):
    file_path = "log.txt"
    try:
        with open(file_path, 'a') as file:
            timestamp = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
            print(message)
            file.write(f"{message} ({timestamp})\n")
    except Exception as e:
        print(f"Failed to write to log: {e}")

async def display_file_content(ctx, file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        await ctx.send(f"```{content}```")
    except FileNotFoundError:
        await ctx.send(f"Datei {file_path} nicht gefunden.")
    except Exception as e:
        await ctx.send(f"Fehler beim Lesen der Datei: {e}")

async def handle_youtube_command(ctx, api_function, number=None, multiple=False):
    if multiple:
        try:
            if number is None:
                await ctx.send("Bitte gib eine Zahl als Parameter an.")
                return
            number = int(number)
            if number > 10:
                await ctx.send("Maximal 10 Memes auf einmal erlaubt.")
                return
            video_urls = api_function(number)
            for video_url in video_urls:
                await ctx.send(video_url)
        except ValueError:
            await ctx.send("Bitte gib eine gültige Zahl ein.")
        except Exception as e:
            await ctx.send(f"Fehler beim Abrufen der YouTube-Videos: {e}")
    else:
        try:
            video_url = api_function() if not number else api_function(number)
            await ctx.send(video_url)
        except Exception as e:
            await ctx.send(f"Fehler beim Abrufen des YouTube-Videos: {e}")

async def send_daily_video(guild_id, video_type):
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(DAILY_CLEARING_CHANNEL_ID)
        if channel and isinstance(channel, discord.TextChannel):
            video_url = youtubeapi() if video_type == 'daily' else youtubeapimemes()
            await channel.send(video_url)

async def send_daily_meme(guild_id):
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(DAILY_CLEARING_CHANNEL_ID)
        if channel and isinstance(channel, discord.TextChannel):
            meme_url = youtubeapimemes()
            await channel.send(meme_url)

async def send_christmas_greeting(guild_id):
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(DAILY_CLEARING_CHANNEL_ID)
        if channel and isinstance(channel, discord.TextChannel):
            greeting = random.choice([
                "Frohe Weihnachten!",
                "Merry Christmas!",
                "Joyeux Noël!",
                "Feliz Navidad!"
            ])
            await channel.send(greeting)

async def send_welcome_message(member, guild_id):
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(YOUR_CHANNEL_ID)
        if channel and isinstance(channel, discord.TextChannel):
            greeting = f"Willkommen auf dem Server, {member.name}!"
            await channel.send(greeting)

async def countdown_process(channel, current_year):
    await asyncio.sleep(30)
    await channel.send("Nicht mehr lang!")
    await asyncio.sleep(20)
    await channel.send("Nur noch 10 Sekunden!")
    await asyncio.sleep(5)
    for i in range(5, 0, -1):
        await channel.send(f"{i}")
        await asyncio.sleep(1)
    await channel.send(f"Frohes Neues Jahr {current_year + 1}!")
    await asyncio.sleep(1)
    await channel.send(f"https://youtu.be/2Mf-53_Y-6E")

async def send_greeting(ctx, night=False):
    if night:
        greeting = random_greeting_night()
    else:
        current_hour = datetime.now().hour + 1
        if 4 <= current_hour <= 11:
            greeting = random_greeting_morning()
        elif 12 <= current_hour <= 17:
            greeting = random_greeting()
        else:
            greeting = random_greeting_evening()
    await ctx.send(greeting)

# Initialisiere den Live-Server (falls benötigt)
live = Live()

# Starte den Bot
bot.run(YOUR_DISCORD_BOT_TOKEN)

