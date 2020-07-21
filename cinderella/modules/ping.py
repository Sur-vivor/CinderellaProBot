import html
import json
import random
import time
import pyowm
from datetime import datetime
from typing import Optional, List

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram import Update, Bot
from telegram.ext import run_async

from cinderella.modules.disable import DisableAbleCommandHandler
from cinderella import dispatcher, StartTime

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
    ping_time = str(round((end_time - start_time), 2) % 60)
    uptime = get_readable_time((time.time() - StartTime))
    update.effective_message.reply_text(f"🏓 Pong!\n⏱️<b>Reply took:</b> {ping_time}s\n🔮<b>Service Uptime:</b> {uptime}", parse_mode=ParseMode.HTML)

@run_async
def uptime(bot: Bot, update: Update):
	uptime = get_readable_time((time.time() - StartTime))
	update.effective_message.reply_text(f"🔮Service Uptime: {uptime}")    

__help__ = """
- /ping :get ping time of bot to telegram server
- /uptime: Find last service update time
"""
__mod_name__ = "PING"

PING_HANDLER = DisableAbleCommandHandler("ping", ping)
UPTIME_HANDLER = DisableAbleCommandHandler("uptime", uptime)
dispatcher.add_handler(UPTIME_HANDLER)
dispatcher.add_handler(PING_HANDLER)
