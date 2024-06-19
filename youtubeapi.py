import random
import os
import json
import urllib.request
import string

def randomyoutubeapi():
  count = 1
  API_KEY = #your_youtubeapi
  random_query = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

  url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={random_query}"

  try:
      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      for video_data in results.get('items', []):
          video_id = video_data['id']['videoId']
          embed_url = f"https://www.youtube.com/embed/{video_id}"
          return embed_url

  except Exception as e:
      return f"Error: {e}"

def ytapi():
  languagen = ["en","de"]
  language = random.choice(languagen)
  count = 1
  API_KEY = #your_youtubeapi
  random_query = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

  url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={random_query}&relevanceLanguage={language}"

  try:
      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      for video_data in results.get('items', []):
          video_id = video_data['id']['videoId']
          embed_url = f"https://www.youtube.com/embed/{video_id}"
          return embed_url

  except Exception as e:
      return f"Error: {e}"

def youtubeapi():
        languagen = ["en","de"]
        language = random.choice(languagen)
        count = 1
        API_KEY = #your_youtubeapi
        random_query = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

        url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={random_query}&relevanceLanguage={language}&videoDuration=medium"

        try:
            with urllib.request.urlopen(url_data) as web_url:
                data = web_url.read()
                encoding = web_url.info().get_content_charset('utf-8')
                results = json.loads(data.decode(encoding))

            for video_data in results.get('items', []):
                video_id = video_data['id']['videoId']
                embed_url = f"https://www.youtube.com/embed/{video_id}"
                return embed_url

        except Exception as e:
            return f"Error: {e}"

def youtubeapilong():
  languagen = ["en","de"]
  language = random.choice(languagen)
  count = 1
  API_KEY = #your_youtubeapi
  random_query = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

  url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={random_query}&relevanceLanguage={language}&videoDuration=long"

  try:
      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      for video_data in results.get('items', []):
          video_id = video_data['id']['videoId']
          embed_url = f"https://www.youtube.com/embed/{video_id}"
          return embed_url

  except Exception as e:
      return f"Error: {e}"

def youtubeshortapi():
  languagen = ["en","de"]
  language = random.choice(languagen)
  count = 1
  API_KEY = #your_youtubeapi
  random_query = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

  url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={random_query}&relevanceLanguage={language}&videoDuration=short"

  try:
      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      for video_data in results.get('items', []):
          video_id = video_data['id']['videoId']
          embed_url = f"https://www.youtube.com/embed/{video_id}"
          return embed_url

  except Exception as e:
      return f"Error: {e}"

def youtubeapisearch(text):
        languagen = ["en","de"]
        language = random.choice(languagen)
        count = 1
        API_KEY = #your_youtubeapi

        meme_query = text

        url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={meme_query}&relevanceLanguage={language}"

        try:
            with urllib.request.urlopen(url_data) as web_url:
                data = web_url.read()
                encoding = web_url.info().get_content_charset('utf-8')
                results = json.loads(data.decode(encoding))

            for video_data in results.get('items', []):
                video_id = video_data['id']['videoId']
                embed_url = f"https://www.youtube.com/embed/{video_id}"
                return embed_url

        except Exception as e:
            return f"Error: {e}"

def youtubeapimemes(number):
  try:
      languagen = ["en" , "de"]
      language = random.choice(languagen)
      count = 100
      API_KEY = #your_youtubeapi1
      if not API_KEY:
          return "API key not found."

      meme_keywords = ["Meme", "Memes", "Dankmemes", "Darkmeme", "Discordmemes", "Memetemplate", "funnymemes",
                       "Funnymeme", "funny", "funny-videos", "Memecompilation", "Offensive-memes", "Random-Memes",
                       "YOU-LAUGH-YOU-FOOL", "Try-Not-to-Laugh", "the-FUNNIEST-videos-on-the-internet",
                       "the-STRANGEST-videos-on-the-internet"]

      meme_query = random.choice(meme_keywords)
      url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={meme_query}&relevanceLanguage={language}&videoDuration=medium"

      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      items = results.get('items', [])
      if items:
          selected_videos = random.sample(items, min(number, len(items)))
          embed_urls = [f"https://www.youtube.com/embed/{video['id']['videoId']}" for video in selected_videos]
          return embed_urls
      else:
          return "No videos found."

  except Exception as e:
      return f"Error: {e}"

def youtubeapimemeslong(number):
  try:
      languagen = ["en", "de"]
      language = random.choice(languagen)
      count = 100
      API_KEY = #your_youtubeapi
      if not API_KEY:
          return "API key not found."

      meme_keywords = ["Meme", "Memes", "Dankmemes", "Darkmeme", "Discordmemes", "Memetemplate", "funnymemes",
                       "Funnymeme", "funny", "funny-videos", "Memecompilation", "Offensive-memes", "Random-Memes",
                       "YOU-LAUGH-YOU-FOOL", "Try-Not-to-Laugh", "the-FUNNIEST-videos-on-the-internet",
                       "the-STRANGEST-videos-on-the-internet"]

      meme_query = random.choice(meme_keywords)
      url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={meme_query}&relevanceLanguage={language}&videoDuration=long"

      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      items = results.get('items', [])
      if items:
          selected_videos = random.sample(items, min(number, len(items)))
          embed_urls = [f"https://www.youtube.com/embed/{video['id']['videoId']}" for video in selected_videos]
          return embed_urls
      else:
          return "No videos found."

  except Exception as e:
      return f"Error: {e}"

def youtubeshortsapimemes(number):
  try:
      languagen = ["en", "de"]
      language = random.choice(languagen)
      count = 100
      API_KEY = #your_youtubeapi
      if not API_KEY:
          return "API key not found."

      meme_keywords = ["Meme", "Memes", "Dankmemes", "Darkmeme", "Discordmemes", "Memetemplate", "funnymemes",
                       "Funnymeme", "funny", "funny-videos", "Memecompilation", "Offensive-memes", "Random-Memes",
                       "YOU-LAUGH-YOU-FOOL", "Try-Not-to-Laugh", "the-FUNNIEST-videos-on-the-internet",
                       "the-STRANGEST-videos-on-the-internet"]

      meme_query = random.choice(meme_keywords)
      url_data = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&maxResults={count}&part=snippet&type=video&q={meme_query}&relevanceLanguage={language}&videoDuration=short"

      with urllib.request.urlopen(url_data) as web_url:
          data = web_url.read()
          encoding = web_url.info().get_content_charset('utf-8')
          results = json.loads(data.decode(encoding))

      items = results.get('items', [])
      if items:
          selected_videos = random.sample(items, min(number, len(items)))
          embed_urls = [f"https://www.youtube.com/embed/{video['id']['videoId']}" for video in selected_videos]
          return embed_urls
      else:
          return "No videos found."
        
  except Exception as e:
      return f"Error: {e}"