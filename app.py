import os
from PIL import Image, ImageFont, ImageDraw
import textwrap
import sqlite3
import praw
import requests
import time
from dotenv import load_dotenv
from imgurpython import ImgurClient

load_dotenv()

conn = sqlite3.connect('stories.db')
conn.execute('''CREATE TABLE IF NOT EXISTS stories
(id TEXT PRIMARY KEY, story TEXT, author TEXT)''')

def create_image(story):
    # Blank Image with White Border
    img = Image.new('RGB', (1280, 1280), color='black')
    border = Image.new('RGB', (1240, 1240), color='white')
    img.paste(border, (20, 20))
    border = Image.new('RGB', (1200, 1200), color='black')
    img.paste(border, (40, 40))
    # Adding small rectangle at bottom
    rect = Image.new('RGB', (300, 40), color='black')
    img.paste(rect, (int((1280/2)-(150)), 1280-40))
    # Adding Branding
    font = ImageFont.truetype('./fonts/Poppins-Bold.ttf', size=36)
    draw = ImageDraw.Draw(img)
    draw.text((int((655)-(150)), 1280-55), "@BOOGY.BOO",
              font=font, fill=(255, 255, 255))
    # Adding Story
    font = ImageFont.truetype('./fonts/Poppins-Regular.ttf', size=35)
    story_lines = textwrap.wrap(story, width=60)
    y_text = int((1280/2)-(len(story_lines)*25))
    for line in story_lines:
        draw.text((1280/2, y_text), line, font=font,
                  fill=(255, 255, 255), anchor="ma")
        y_text += 50
    img.save('output.png')

def get_story():
    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent="Boogy Boo"
    )
    # Get top weekly submissions for cute animals
    submissions = reddit.subreddit('TwoSentenceHorror').top('week', limit=10)
    for submission in submissions:
        id = submission.id
        story = submission.title + " " + submission.selftext
        author = submission.author.name
        if not is_posted(id):
            return (id, story, author)
        else:
            continue

def upload_to_imgur():
    imgur = ImgurClient(os.getenv('IMGUR_ID'), os.getenv('IMGUR_SECRET'))
    image = imgur.upload_from_path('output.png', anon=True)
    return image['link']

def upload_to_instagram(url, caption):
    r1 = requests.post(
        f"https://graph.facebook.com/v13.0/{os.getenv('IG_PAGE_ID')}/media?image_url={url}&caption={caption}&access_token={os.getenv('FB_ACCESS_TOKEN')}")
    if r1.status_code != 200:
        print(r1.json())
        return False
    creation_id = r1.json()['id']
    r2 = requests.post(
        f"https://graph.facebook.com/v13.0/{os.getenv('IG_PAGE_ID')}/media_publish?creation_id={creation_id}&access_token={os.getenv('FB_ACCESS_TOKEN')}")
    if r2.status_code != 200:
        print(r2.json())
        return False
    return True

def is_posted(id):
    if conn.execute("SELECT * FROM stories WHERE id=?", (id,)).fetchone() is None:
        return False
    return True

def update_db(id, story, author):
    if conn.execute("SELECT * FROM stories WHERE id=?", (id,)).fetchone() is None:
        conn.execute(
            "INSERT OR IGNORE INTO stories VALUES (?, ?, ?)", (id, story, author))
        conn.commit()

if __name__ == "__main__":
    id, story, author = get_story()
    time.sleep(5)
    create_image(story)
    url = upload_to_imgur()
    time.sleep(5)
    if upload_to_instagram(url, "Story by r/" + author+"\n\n%23horror %23spooky %23weird %23scary %23creepy %23satan %23fear  %23scare %23creepypicture %23horrorstory %23follow4follow %23like4like %23l4l %23f4f %23photooftheday %23followme %23creepypasta"):
        update_db(id, story, author)
        print("Posted to Instagram")