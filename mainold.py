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

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='', intents=intents)  # Set a command prefix

# Define start_time at the beginning
start_time = datetime.now()

# Set the daily clearing channel ID here
DAILY_CLEARING_CHANNEL_ID = #your_cannelid

# Use a dictionary to store server-specific states instead of global variables
daily_video_online = {}
happycrismas = {}

@tasks.loop(minutes=5)
async def update_time():
    os.system('clear' if os.name == 'posix' else 'cls')
    elapsed_time = datetime.now() - start_time
    elapsed_minutes = int(elapsed_time.total_seconds() / 60)
    global time 
    time = elapsed_minutes
    activity = discord.Game(name=f"seit {round(elapsed_minutes/60)}h", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    current_hour = datetime.now().hour + 1
    current_minute = datetime.now().minute
    current_second = datetime.now().second
  
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Use the server ID as the key for server-specific states
    guild_id = #your_server_id
    if guild_id not in daily_video_online:
        daily_video_online[guild_id] = False

    if current_hour == 18:
      if daily_video_online[guild_id] != True:
          a = random.randint(1,100)
          if a >= 95:
              v = "rl"
          elif a >= 70:
              v = "r"
          elif a >= 40:
              v = "v"
          else:
              v = "s"
          a = random.randint(1,100)
          if a <= 1:
              r = 2
          else:
              r = 1
          channel_id = #your_channel_id
          guild = bot.get_guild(guild_id) 
          if guild:
              channel = guild.get_channel(channel_id)
              if channel and isinstance(channel, discord.TextChannel):
                  if v == "v":
                    await channel.send("Hier sind die täglichen normalen Videos" + ": " + str(youtubeapimemes(r)) + " (Wenn ihr mehr wollt schreibt mir einfach youtubememe, im Bot chat oder per dm)) ")
                  elif v == "s":
                    await channel.send("Hier sind die täglichen kurzen Videos" + ": " + str(youtubeshortsapimemes(r)) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutubememe, im Bot chat oder per dm) ")
                  elif v == "r":
                    await channel.send("Hier sind die täglichen random Videos: " + str(youtubeshortapi()) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutube, im Bot chat oder per dm) ")
                  elif v == "rl":
                     await channel.send("Hier sind die täglichen langen random Videos: " + str(youtubeapilong()) + " (Wenn ihr mehr wollt schreibt mir einfach shortyoutube, im Bot chat oder per dm) ")
                  print("Daily Video is jetzt online")
                  daily_video_online[guild_id] = True

    elif current_hour == 20:
      if daily_video_online[guild_id] != True:
          channel_id = #your_channel_id
          guild = bot.get_guild(guild_id) 
          if guild:
              channel = guild.get_channel(channel_id)
              if channel and isinstance(channel, discord.TextChannel):
                  respons = requests.get("https://meme-api.com/gimme")
                  json_data = json.loads(respons.text)
                  await channel.send("Hier ist das tägliche random Meme:" + json_data['url'] + " (Wenn ihr mehr wollt schreibt mir einfach meme, im Bot chat oder per dm) ")
                  daily_video_online[guild_id] = True

    elif current_month == 12 and current_day == 24 and current_hour == 12:
      if daily_video_online[guild_id] != True:
            channel_id = #your_channel_id
            guild = bot.get_guild(guild_id) 
            if guild:
                channel = guild.get_channel(channel_id)
                if channel and isinstance(channel, discord.TextChannel):
                    out = ["Ich wünsche euch frohe Weihnachten, @everyone", "Frohe Weihnachten, @everyone", "Merry Chrismas , @everyone", "Happy Christmas, @everyone"]
                    o = random.choice(out)
                    await channel.send(o)
                    print("Merry Christmas")
                    daily_video_online[guild_id] = True
                  
    elif current_month == 12 and current_day == 31 and current_hour == 23 and 55 >= current_minute >= 50:
      if daily_video_online[guild_id] != True:
        # Start a new asyncio task to run the countdown without blocking the event loop
        bot.loop.create_task(countdown())
        daily_video_online[guild_id] = True
        
    else:
      daily_video_online[guild_id] = False
    print(f"Aktualisierte Zeit: {elapsed_minutes}min ( {current_day}.{current_month}.{current_year} )( {current_hour}:{current_minute}:{current_second} ) ( Daily Video {daily_video_online[guild_id]} ) Nächste Aktualisierung in 5 min ")

@bot.event
async def on_ready():
    file_path = "log.txt"
    try:
      with open(file_path, 'a') as file:  # 'a' stands for append mode
          current_hour = datetime.now().hour + 1
          current_minute = datetime.now().minute
          current_second = datetime.now().second
          current_day = datetime.now().day
          current_month = datetime.now().month
          current_year = datetime.now().year
          print("Bot is ready!")
          file.write(f"Bot is started! ( {current_hour}:{current_minute}:{current_second} ) ( {current_day}.{current_month}.{current_year} ) " + '\n')  # Add a newline after each entry
    except Exception as e:
      print("fail to write to log on start")
    
    update_time.start()

@bot.event
async def on_member_join(member):
  try:
    guild_id = #your_server_id
    if guild_id:
      guild = bot.get_guild(guild_id) 
      # Hier kannst du die Willkommensnachricht anpassen
      channel_id = #your_channel_id  # Setze die ID des Kanals, in dem die Nachricht gesendet werden soll
      channel = guild.get_channel(channel_id)
      if channel:
          welcome_message = f'Willkommen auf dem Server, {member.mention}!'
          role = [#your_random_role_id, your_random_role_id, 
             ]
        
          # Wähle eine zufällige Rolle aus
          role_id = random.choice(role)
    
          # Hole die Rolle nach ID
          role = member.guild.get_role(role_id)

          try:
              # Pfad zur Datei, die die Anzahl der Ausführungen speichert
              count_file = "zahldatei.txt"
  
              # Überprüfen, ob die Zähldatei existiert
              if not os.path.exists(count_file):
                  with open(count_file, 'w') as file:
                      file.write("0")
  
              # Aktuelle Anzahl der Ausführungen aus der Zähldatei lesen
              with open(count_file, 'r') as file:
                  count = int(file.read())
  
              # Inkrementiere den Zähler
              count += 1
  
              # Ausgabe der aktuellen Ausführungsanzahl
              countmessage = f'Und du bist der {count}. der dem Server joint!'
  
              # Speichere die aktualisierte Ausführungsanzahl in der Zähldatei
              with open(count_file, 'w') as file:
                  file.write(str(count))
                
          except Exception as e:  
            print("fail to write to count")
            countmessage = ""

          try:
            # Pfad zur Datei, die die Anzahl der Ausführungen speichert
            count_file = "zahldatei.txt"

            # Aktuelle Anzahl der Ausführungen aus der Zähldatei lesen
            with open(count_file, 'r') as file:
                count = int(file.read())

            new_name = str(member.display_name) + " " + str(count)
            await member.edit(nick=new_name)

          except Exception as e:  
            print("fail to give nickname")
            
          if role:
            welcome_message = f'Willkommen auf dem Server, {member.display_name}! Du bist eine, {role.name}! {countmessage}'
            await channel.send(welcome_message)
  
            # Rolle dem Mitglied hinzufügen
            await member.add_roles(role)
            file_path = "memberlog.txt"
              
            try:
              with open(file_path, 'a') as file:  # 'a' stands for append mode
                  current_hour = datetime.now().hour + 1
                  current_minute = datetime.now().minute
                  current_second = datetime.now().second
                  current_day = datetime.now().day
                  current_month = datetime.now().month
                  current_year = datetime.now().year
                  print(f'Die Rolle {role.name} wurde {member.display_name} hinzugefügt.')
                  file.write(f'Die Rolle {role.name} wurde zu {member.display_name} hinzugefügt. ( {current_hour}:{current_minute}:{current_second} ) ( {current_day}.{current_month}.{current_year} )' + '\n')  # Add a newline after each entry
            except Exception as e:  
              print("fail to write to log")
      
  except Exception as e:
    print(f"An error occurred: {e}")

@bot.command()
async def countdownxyz(ctx):
  bot.loop.create_task(countdown())

async def countdown():
    current_year = datetime.utcnow().year
    guild_id = #your_server_id
    channel_id = #your_channel_id
    guild = bot.get_guild(guild_id)
    if guild:
        channel = guild.get_channel(channel_id)
        if channel and isinstance(channel, discord.TextChannel):
            await channel.send("Nicht mehr lang bis " + str(current_year + 1))
            start_hour = datetime.utcnow().hour
            while True:
                current_minute = datetime.utcnow().minute
                countdowntime_minute = 60 - current_minute
                if countdowntime_minute == 60:
                    current_second = datetime.utcnow().second
                    last_second = current_second
                    if last_second <= 1:
                      await asyncio.sleep(3)
                    while True:
                        current_hour = datetime.utcnow().hour
                        current_second = datetime.utcnow().second
                        countdowntime_second = 60 - current_second
                        if last_second != current_second:
                          last_second = current_second
                          print(str(countdowntime_second))
                          if countdowntime_second == 59:
                              await asyncio.sleep(1)
                              await clear_messages(channel, 12)
                              await asyncio.sleep(1)
                              await channel.send(f"Ich wünsche euch ein, fröhliches {current_year + 1}, @everyone")
                              break
                          elif countdowntime_second == 60:
                            await channel.send("Null")
                          elif 0 < countdowntime_second < 11:
                            await channel.send(str(countdowntime_second))
                    break
                elif countdowntime_minute == 5:
                    await channel.send("noch 5 minuten bis " + str(current_year + 1))
                    await asyncio.sleep(60)
                else:
                    print(str(countdowntime_minute))
                    await asyncio.sleep(30)
                    
@bot.command()
async def displaylog(ctx):
  file_path = "log.txt"
  try:
    with open(file_path, 'r') as file:
        file_content = file.read()
        await ctx.send(f"Content of the file {file_path}:\n```\n{file_content}\n```")
  except FileNotFoundError:
    await ctx.send(f"The file {file_path} does not exist.")
  except Exception as e:
    await ctx.send(f"An error occurred while reading the file: {e}")

@bot.command()
async def displaymemberlog(ctx):
  file_path = "memberlog.txt"
  try:
    with open(file_path, 'r') as file:
        file_content = file.read()
        await ctx.send(f"Content of the file {file_path}:\n```\n{file_content}\n```")
  except FileNotFoundError:
    await ctx.send(f"The file {file_path} does not exist.")
  except Exception as e:
    await ctx.send(f"An error occurred while reading the file: {e}")

#youtube
@bot.command()
async def youtube(ctx):
    try:
        await ctx.send(youtubeapi())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

#youtube
@bot.command()
async def randomyoutube(ctx):
    try:
        await ctx.send(randomyoutubeapi())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def yt(ctx):
    try:
        await ctx.send(ytapi())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def longyoutube(ctx):
    try:
        await ctx.send(youtubeapilong())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def shortyoutube(ctx):
    try:
        await ctx.send(youtubeshortapi())
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def youtubememe(ctx):
    try:
        number = 1
        await ctx.send(youtubeapimemes(number))
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def longyoutubememe(ctx):
    try:
        number = 1
        await ctx.send(youtubeapimemeslong(number))
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def shortyoutubememe(ctx):
    try:
        number = 1
        await ctx.send(youtubeshortsapimemes(number))
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def youtubememes(ctx, number=None):
    try:
        if number is None:
            number = "1"

        num = int(number)
        if num > 10:
            num = 10
            await ctx.send("Maximal 10 Memes. sending...")
            await asyncio.sleep(5)

        video_urls = youtubeapimemes(num)

        for url in video_urls:
            await ctx.send(url)

    except ValueError:
        await ctx.send("Please provide a valid number.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def longyoutubememes(ctx, number=None):
    try:
        if number is None:
            number = "1"

        num = int(number)
        if num > 10:
            num = 10
            await ctx.send("Maximal 10 Memes. sending...")
            await asyncio.sleep(5)

        video_urls = youtubeapimemeslong(num)

        for url in video_urls:
            await ctx.send(url)

    except ValueError:
        await ctx.send("Please provide a valid number.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def shortyoutubememes(ctx, number=None):
    try:
        if number is None:
            number = "1"

        num = int(number)
        if num > 10:
            num = 10
            await ctx.send("Maximal 10 Memes. sending...")
            await asyncio.sleep(5)

        video_urls = youtubeshortsapimemes(num)

        for url in video_urls:
            await ctx.send(url)

    except ValueError:
        await ctx.send("Please provide a valid number.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def search(ctx, text):
    try:
        await ctx.send(youtubeapisearch(text))
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

#toilette meme
@bot.command()
async def toilette(ctx):
    await ctx.send("https://youtu.be/3DpjtBWYifg?si=2NnvHDZky2meF5dH")

#meme
@bot.command()
async def meme(ctx):
    respons = requests.get("https://meme-api.com/gimme")
    json_data = json.loads(respons.text)
    await ctx.send(json_data.get("url"))

#Begrüßungen
@bot.command()
async def hallo(ctx):
  hour = datetime.now().hour + 1
  if hour >= 5 and hour <= 12:
    await ctx.send(random_greeting_morning())
  elif hour >= 13 and hour <= 17:
    await ctx.send(random_greeting())
  elif hour >= 18 and hour <= 21:
    await ctx.send(random_greeting_evening())
  else:
    await ctx.send(random_greeting())

@bot.command()
async def hey(ctx):
  hour = datetime.now().hour + 1
  if hour >= 5 and hour <= 12:
    await ctx.send(random_greeting_morning())
  elif hour >= 13 and hour <= 17:
    await ctx.send(random_greeting())
  elif hour >= 18 and hour <= 21:
    await ctx.send(random_greeting_evening())
  else:
    await ctx.send(random_greeting())

@bot.command()
async def na(ctx):
  hour = datetime.now().hour + 1
  if hour >= 5 and hour <= 12:
    await ctx.send(random_greeting_morning())
  elif hour >= 13 and hour <= 17:
    await ctx.send(random_greeting())
  elif hour >= 18 and hour <= 21:
    await ctx.send(random_greeting_evening())
  else:
    await ctx.send(random_greeting_night)

@bot.command()
async def moin(ctx):
  hour = datetime.now().hour + 1
  if hour >= 5 and hour <= 12:
    await ctx.send(random_greeting_morning())
  elif hour >= 13 and hour <= 17:
    await ctx.send(random_greeting())
  elif hour >= 18 and hour <= 21:
    await ctx.send(random_greeting_evening())
  else:
    await ctx.send(random_greeting_night())

@bot.command()
async def hi(ctx):
  hour = datetime.now().hour + 1
  if hour >= 5 and hour <= 12:
    await ctx.send(random_greeting_morning())
  elif hour >= 13 and hour <= 17:
    await ctx.send(random_greeting())
  elif hour >= 18 and hour <= 21:
    await ctx.send(random_greeting_evening())
  else:
    await ctx.send(random_greeting_night())

@bot.command()
async def write(ctx, text):await ctx.send(text)

#Begrüßung andere Sprachen
@bot.command()
async def hello(ctx):
    await ctx.send(random_language())

@bot.command()
async def sus(ctx):
  await ctx.send("https://youtu.be/keyRM3h_7tk?si=eIIx3UGRqVKThGsi")

@bot.command()
async def imposter(ctx):
  await ctx.send("https://youtu.be/RMyFf73Stoc?si=P_H3VNaiENCyBmUL")

#clear
async def clearchannel(ctx, limit: int = 5):  # Set a default limit of 10 if not provided
  channel = ctx.message.channel
  
  if not channel:
    print("Invalid channel ID provided.")
  else:
    # Check if there are messages in the channel
    while True:
      # Call the function to clear messages with the retry mechanism
      await clear_messages(channel, 5)
      channel = ctx.message.channel
      # Check if there are no more messages in the channel
      if not channel.last_message:
          break
      await asyncio.sleep(10)
  print(f"All cleared in channel {channel.name}")

async def clear_messages(channel, limit):
    try:
        # Fetch messages and delete them
        async for message in channel.history(limit=limit):
            await message.delete()

        print(f"Channel ({channel}) got a lite bit cleared.")
    except discord.Forbidden:
        print("Bot does not have the necessary permissions to delete messages.")
    except discord.HTTPException as e:
        if e.status == 429:  # Check if it's a rate limit error
            retry_after = e.retry_after
            print(f"Rate limited. Retrying in {retry_after} seconds.")
            await clear_messages(channel, limit)  # Retry the operation
        else:
            print(f"An error occurred while deleting messages: {e}")


Live(start_time) 
bot.run(#your_Discordbottoken
   )
