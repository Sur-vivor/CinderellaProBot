import html
import json
import random
import time
import pyowm
from pyowm import timeutils, exceptions
from datetime import datetime
from typing import Optional, List

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram import Update, Bot
from telegram.ext import run_async

from alluka.modules.disable import DisableAbleCommandHandler
from alluka import dispatcher, StartTime

from requests import get

def get_readable_time(seconds: int) -> str:

    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
        
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
@run_async
def ping(bot: Bot, update: Update):
    start_time = time.time()
    requests.get('https://api.telegram.org')
    end_time = time.time()
    ms = float(end_time - start_time)
    update.effective_message.reply_text("🏓 Pong!\n⏱️Reply took: {0:.2f}s".format(round(ms, 2) % 60), parse_mode=ParseMode.MARKDOWN)

@run_async
def uptime(bot: Bot, update: Update):
	uptime = get_readable_time((time.time() - StartTime))
	update.effective_message.reply_text(f"Çΐή∂εɾεℓℓส uptime: {uptime}")    
    

__mod_name__ = "Ping"

PING_HANDLER = DisableAbleCommandHandler("ping", ping)
UPTIME_HANDLER = DisableAbleCommandHandler("uptime", uptime)
dispatcher.add_handler(UPTIME_HANDLER)
dispatcher.add_handler(PING_HANDLER)
