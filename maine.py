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

# Define your constants here
DAILY_CLEARING_CHANNEL_ID = os.getenv('DAILY_CLEARING_CHANNEL_ID')  # Replace with your channel ID
YOUR_SERVER_ID = os.getenv('YOUR_SERVER_ID')  # Replace with your server ID
YOUR_CHANNEL_ID = os.getenv('YOUR_CHANNEL_ID')  # Replace with your channel ID
YOUR_DISCORD_BOT_TOKEN = os.getenv('YOUR_DISCORD_BOT_TOKEN')  # Replace with your Discord bot token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='', intents=intents)

start_time = datetime.now()
daily_video_online = {}
happycrismas = {}

@tasks.loop(minutes=5)
async def update_time():
    os.system('clear' if os.name == 'posix' else 'cls')
    elapsed_time = datetime.now() - start_time
    elapsed_minutes = int(elapsed_time.total_seconds() / 60)
    activity = discord.Game(name=f"seit {round(elapsed_minutes/60)}h", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    current_hour = datetime.now().hour + 1
    current_minute = datetime.now().minute
    current_second = datetime.now().second

    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    guild_id = YOUR_SERVER_ID
    if guild_id not in daily_video_online:
        daily_video_online[guild_id] = False

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
    log_event("Bot is ready!")
    update_time.start()

@bot.event
async def on_member_join(member):
    guild_id = YOUR_SERVER_ID
    if guild_id:
        await send_welcome_message(member, guild_id)

@bot.command()
async def countdownxyz(ctx):
    bot.loop.create_task(countdown())

async def countdown():
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
    await display_file_content(ctx, "log.txt")

@bot.command()
async def displaymemberlog(ctx):
    await display_file_content(ctx, "memberlog.txt")

# youtube commands
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

# commands for fun and greetings
@bot.command()
async def toilette(ctx):
    await ctx.send("https://youtu.be/3DpjtBWYifg?si=2NnvHDZky2meF5dH")

@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme")
    json_data = json.loads(response.text)
    await ctx.send(json_data.get("url"))

# greeting commands
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

# greeting in different languages
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

# Helper functions
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
            file_content = file.read()
            await ctx.send(f"Content of the file {file_path}:\n```\n{file_content}\n```")
    except FileNotFoundError:
        await ctx.send(f"The file {file_path} does not exist.")
    except Exception as e:
        await ctx.send(f"An error occurred while reading the file: {e}")

async def send_daily_video(guild_id, video_type):
    video_options = ['v', 's', 'r', 'rl']
    video_probabilities = [40, 30, 25, 5]
    video_choice = random.choices(video_options, video_probabilities)[0]

    channel_id = YOUR_CHANNEL_ID
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            if video_choice == 'v':
                await channel.send("Hier sind die täglichen normalen Videos: " + str(youtubeapimemes(1)) + " (Wenn ihr mehr wollt schreibt mir einfach youtubememe, im Bot chat oder per dm)")
            elif video_choice == 's':
                await channel.send("Hier sind die täglichen kurzen Videos: " + str(youtubeshortsapimemes(1)) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutubememe, im Bot chat oder per dm)")
            elif video_choice == 'r':
                await channel.send("Hier sind die täglichen random Videos: " + str(youtubeshortapi()) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutube, im Bot chat oder per dm)")
            elif video_choice == 'rl':
                await channel.send("Hier sind die täglichen langen random Videos: " + str(youtubeapilong()) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutube, im Bot chat oder per dm)")
            daily_video_online[guild_id] = True

async def send_daily_meme(guild_id):
    channel_id = YOUR_CHANNEL_ID
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            response = requests.get("https://meme-api.com/gimme")
            json_data = json.loads(response.text)
            await channel.send("Hier ist das tägliche random Meme:" + json_data['url'] + " (Wenn ihr mehr wollt schreibt mir einfach meme, im Bot chat oder per dm)")
            daily_video_online[guild_id] = True

async def send_christmas_greeting(guild_id):
    channel_id = YOUR_CHANNEL_ID
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            greetings = ["Ich wünsche euch frohe Weihnachten, @everyone", "Frohe Weihnachten, @everyone", "Merry Christmas, @everyone", "Happy Christmas, @everyone"]
            greeting = random.choice(greetings)
            await channel.send(greeting)
            daily_video_online[guild_id] = True

async def send_welcome_message(member, guild_id):
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(YOUR_CHANNEL_ID)
        if channel:
            welcome_message = f'Willkommen auf dem Server, {member.mention}!'
            roles = [YOUR_RANDOM_ROLE_ID_1, YOUR_RANDOM_ROLE_ID_2]  # Replace with your role IDs
            role_id = random.choice(roles)
            role = member.guild.get_role(role_id)

            count = increment_join_count()

            try:
                new_name = f"{member.display_name} {count}"
                await member.edit(nick=new_name)
            except Exception as e:
                print(f"Failed to give nickname: {e}")

            if role:
                welcome_message = f'Willkommen auf dem Server, {member.display_name}! Du bist eine, {role.name}! Und du bist der {count}. der dem Server joint!'
                await channel.send(welcome_message)
                await member.add_roles(role)
                log_event(f'Die Rolle {role.name} wurde zu {member.display_name} hinzugefügt.')

def increment_join_count():
    count_file = "zahldatei.txt"
    try:
        if not os.path.exists(count_file):
            with open(count_file, 'w') as file:
                file.write("0")
        with open(count_file, 'r') as file:
            count = int(file.read())
        count += 1
        with open(count_file, 'w') as file:
            file.write(str(count))
        return count
    except Exception as e:
        print(f"Failed to increment join count: {e}")
        return 0

async def countdown_process(channel, current_year):
    await channel.send(f"Nicht mehr lang bis {current_year + 1}")
    start_hour = datetime.utcnow().hour
    while True:
        current_minute = datetime.utcnow().minute
        countdown_minutes = 60 - current_minute
        if countdown_minutes == 60:
            await countdown_seconds(channel, current_year)
            break
        elif countdown_minutes == 5:
            await channel.send(f"noch 5 Minuten bis {current_year + 1}")
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)

async def countdown_seconds(channel, current_year):
    await asyncio.sleep(1)
    await clear_messages(channel, 12)
    await asyncio.sleep(1)
    await channel.send(f"Ich wünsche euch ein fröhliches {current_year + 1}, @everyone")
    await asyncio.sleep(1)
    for i in range(10, 0, -1):
        await channel.send(str(i))
        await asyncio.sleep(1)
    await channel.send("Null")

async def send_greeting(ctx, night=False):
    hour = datetime.now().hour + 1
    if 5 <= hour <= 12:
        await ctx.send(random_greeting_morning())
    elif 13 <= hour <= 17:
        await ctx.send(random_greeting())
    elif 18 <= hour <= 21:
        await ctx.send(random_greeting_evening())
    elif night:
        await ctx.send(random_greeting_night())
    else:
        await ctx.send(random_greeting())

async def handle_youtube_command(ctx, api_func, *args, limit=False):
    try:
        if limit and args:
            num = int(args[0])
            if num > 10:
                num = 10
                await ctx.send("Maximal 10 Memes. sending...")
                await asyncio.sleep(5)
            args = (num,)
        result = api_func(*args)
        if isinstance(result, list):
            for item in result:
                await ctx.send(item)
        else:
            await ctx.send(result)
    except ValueError:
        await ctx.send("Please provide a valid number.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

Live(start_time)
bot.run(YOUR_DISCORD_BOT_TOKEN)
