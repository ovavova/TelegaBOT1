#telegram bot for reposting Reddit contecnt weekly
#
#TELEGRAM BOT INFO:

#Done! Congratulations on your new bot.
# You will find it at t.me/funnyNSFWred_bot. @funnyNSFWred_bot
# You can now add a description, about section and profile picture for
# your bot, see /help for a list of commands.
# By the way, when you've finished creating your cool bot,
# ping our Bot Support if you want a better username for it.
# Just make sure the bot is fully operational before you do this.
#
#Use this token to access the HTTP API:
#2028118352:AAH3E56XziDN_qavu1VcCb-zpNdI16FoF2c
#Keep your token secure and store it safely,
# it can be used by anyone to control your bot.
#
#For a description of the Bot API, see this page: https://core.telegram.org/bots/api
#
#Reddit app
#Name:funnyNSFWred_bot
#http://localhost:8080
#web app CQUKnI2UJ26rJ-c8mhoQ4A
#secret	qAapwg04_2IhUAxstKUoC4yrMK3EWg
#developers	ovavova (that's you!) remove
#
from __future__ import unicode_literals

import telegram
import praw
import logging
import html
import sys
import os
import json

from time import sleep
from datetime import datetime

credentials = {}

credentials["token"] = os.environ.get('TOKEN')
credentials["subreddit"] = os.environ.get('SUB')
credentials["channel"] = os.environ.get('CHANNEL')

log = logging.getLogger('doggo')
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

if credentials["token"] == "":
    raise RuntimeError('Bot token not found 🙁! Put bot token🔐 in credentials.json!')
if credentials["subreddit"] == "":
    raise RuntimeError('Subreddit name not found 🙁! Enter the subreddit name📃 in credentials.json!')
if credentials["channel"] == "":
    raise RuntimeError('Telegram Channel name not found 🙁! Enter the channel name📰 in credentials.json!')

token = credentials["token"]
channel = credentials["channel"]
sub = "dogpictures"
start_time = datetime.utcnow().timestamp()

def prev_submissions():
    try:
        with open('prev_submissions.id', 'r') as f:
            return f.read().strip()
    except:
        return None

def write_submissions(sub_id):
    try:
        with open('prev_submissions.id', 'w') as f:
            f.write(sub_id)
    except:
        log.expection("Error writing sub ID!")

post = False
last_sub_id = prev_submissions()

if not last_sub_id:
    log.info("Latest submission not found, starting all submissions!")
    post = True
else:
    log.info("Last posted submission is {}".format(last_sub_id))

r = praw.Reddit(user_agent="Dank Doggo by Harsha :D",
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET'),
                username=os.environ.get('RUSERNAME'),
                password=os.environ.get('RPASS'))
r.read_only = True
subreddit = r.subreddit(sub)

bot = telegram.Bot(token=token)
# for submission in subreddit.stream.submissions():
#     print(submission.url)

while True:
    try:
        for submission in subreddit.hot():
            try:
                link = "https://redd.it/{id}".format(id=submission.id)
                if not post and submission.created_utc < start_time:
                    log.info("Skipping {} --- latest submission not found!".format(submission.id))
                    if submission.id == last_sub_id:
                        post = True
                    continue
                image = html.escape(submission.url or '')
                title = html.escape(submission.title or '')
                user = html.escape(submission.author.name or '')

                template = "{title}\n{link}\nby {user}"
                message = template.format(title=title, link=link, user=user)

                log.info("Posting {}".format(link))
                bot.sendPhoto(chat_id=channel, photo=submission.url, caption=message)
                # bot.sendMessage(chat_id=channel, parse_mode=telegram.ParseMode.HTML, text=message)
                write_submissions(submission.id)
                sleep(300)
            except Exception as e:
                log.exception("Error parsing {}".format(link))
    except Exception as e:
        log.exception("Error fetching new submissions, restarting in 10 secs")
        sleep(10)