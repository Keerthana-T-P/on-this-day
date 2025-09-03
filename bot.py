import os
import requests
import datetime
import random
import tweepy
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load .env
load_dotenv()

# Auth for v1.1 (media upload)
auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"),
    os.getenv("API_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_SECRET")
)
api = tweepy.API(auth)

# Auth for v2 (tweeting)
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

def get_history_events():
    today = datetime.datetime.now()
    url = f"http://history.muffinlabs.com/date/{today.month}/{today.day}"
    res = requests.get(url).json()
    events = res["data"]["Events"]
    return random.sample(events, 3)

def create_image_card(facts):
    today = datetime.datetime.now().strftime("%b %d, %Y")

    img = Image.new("RGB", (1200, 628), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 48)
        fact_font = ImageFont.truetype("arial.ttf", 32)
        footer_font = ImageFont.truetype("ariali.ttf", 28)
    except:
        title_font = fact_font = footer_font = ImageFont.load_default()

    draw.text((50, 40), f"📅 On This Day - {today}", font=title_font, fill=(20, 20, 20))

    y = 120
    for f in facts:
        text = f"• {f['year']}: {f['text']}"
        draw.text((50, y), text, font=fact_font, fill=(40, 40, 40))
        y += 100

    footer = "Meanwhile in 2025, you’re still waiting for flying cars. 🚗✨"
    draw.text((50, 550), footer, font=footer_font, fill=(120, 120, 120))

    filename = "today_card.png"
    img.save(filename)
    return filename

def post_tweet_with_image():
    facts = get_history_events()
    filename = create_image_card(facts)

    try:
        media = api.media_upload(filename)  # v1.1 upload
        client.create_tweet(text="", media_ids=[media.media_id])  # v2 post
        print("✅ Tweet with image card posted successfully!")
    except Exception as e:
        print("❌ Error posting tweet:", e)
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Run
post_tweet_with_image()
