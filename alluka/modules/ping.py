import html
import json
from datetime import datetime
from typing import Optional, List
import requests
import subprocess
import os
import speedtest
import time
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from alluka.modules.helper_funcs.extraction import extract_text

from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS
from alluka.modules.helper_funcs.filters import CustomFilters

#Kanged from PaperPlane Extended userbot
def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

@run_async
def get_bot_ip(bot: Bot, update: Update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)

@run_async
def rtt(bot: Bot, update: Update):
    out = ""
    under = False
    if os.name == 'nt':
        output = subprocess.check_output("ping -n 1 1.0.0.1 | findstr time*", shell=True).decode()
        outS = output.splitlines()
        out = outS[0]
    else:
        out = subprocess.check_output("ping -c 1 1.0.0.1 | grep time=", shell=True).decode()
    splitOut = out.split(' ')
    stringtocut = ""
    for line in splitOut:
        if(line.startswith('time=') or line.startswith('time<')):
            stringtocut=line
            break
    newstra=stringtocut.split('=')
    if len(newstra) == 1:
        under = True
        newstra=stringtocut.split('<')
    newstr=""
    if os.name == 'nt':
        newstr=newstra[1].split('ms')
    else:
        newstr=newstra[1].split(' ') #redundant split, but to try and not break windows ping
    ping_time = float(newstr[0])
    if os.name == 'nt' and under:
        update.effective_message.reply_text(" Round-trip time is <{}ms".format(ping_time))
    else:
        update.effective_message.reply_text(" Round-trip time: {}ms".format(ping_time))

def ping(bot: Bot, update: Update):
    message = update.effective_message
    parsing = extract_text(message).split(' ')
    if(len(parsing) < 2):
        message.reply_text("Give me an address to ping!")
        return
    elif(len(parsing)>2):
        message.reply_text("Too many arguments!")
        return
    dns = (parsing)[1]
    out = ""
    under = False
    if os.name == 'nt':
        try:
            output = subprocess.check_output("ping -n 1 " + dns + " | findstr time*", shell=True).decode()
        except:
            message.reply_text("There was a problem parsing the IP/Hostname")
            return
        outS = output.splitlines()
        out = outS[0]
    else:
        try:
            out = subprocess.check_output("ping -c 1 " + dns + " | grep time=", shell=True).decode()
        except:
            message.reply_text("There was a problem parsing the IP/Hostname")
            return
    splitOut = out.split(' ')
    stringtocut = ""
    for line in splitOut:
        if(line.startswith('time=') or line.startswith('time<')):
            stringtocut=line
            break
    newstra=stringtocut.split('=')
    if len(newstra) == 1:
        under = True
        newstra=stringtocut.split('<')
    newstr=""
    if os.name == 'nt':
        newstr=newstra[1].split('ms')
    else:
        newstr=newstra[1].split(' ') #redundant split, but to try and not break windows ping
    ping_time = float(newstr[0])
    if os.name == 'nt' and under:
        update.effective_message.reply_text(" Ping speed of " +dns+" is <{}ms".format(ping_time))
    else:
        update.effective_message.reply_text(" Ping speed of " +dns+": {}ms".format(ping_time))
    
    

@run_async
def speedtst(bot: Bot, update: Update):
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    update.effective_message.reply_text("Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}")

IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID))
RTT_HANDLER = CommandHandler("ping", rtt, filters=CustomFilters.sudo_filter)
PING_HANDLER = CommandHandler("cping", ping, filters=CustomFilters.sudo_filter)
SPEED_HANDLER = CommandHandler("tsp", speedtst, filters=CustomFilters.sudo_filter) 

dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(RTT_HANDLER)
dispatcher.add_handler(SPEED_HANDLER)
dispatcher.add_handler(PING_HANDLER)
import html
import jsonimport html
import json
import os
import psutil
import random
import time
import datetime
from typing import Optional, List
import re
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from alluka.modules.helper_funcs.chat_status import user_admin, sudo_plus, is_user_admin
from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS, WHITELIST_USERS, BAN_STICKER
from alluka.__main__ import STATS, USER_INFO, TOKEN
from alluka.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from alluka.modules.helper_funcs.extraction import extract_user
from alluka.modules.helper_funcs.filters import CustomFilters
import alluka.modules.sql.users_sql as sql

@run_async
def info(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not message.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    text = (f"<b>Characteristics:</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"First Name: {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\nLast Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\nUsername: @{html.escape(user.username)}"

    text += f"\nPermanent user link: {mention_html(user.id, 'link')}"

    num_chats = sql.get_user_num_chats(user.id)
    text += f"\nChat count: <code>{num_chats}</code>"

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\nThis user holds the title <b>{custom_title}</b> here."
    except BadRequest:
        pass

   

    if user.id == OWNER_ID:
        text += "\nThis person is my owner - I would never do anything against them!."
        
    elif user.id in DEV_USERS:
        text += "\nThis person is my dev - I would never do anything against them!."
        
    elif user.id in SUDO_USERS:
        text += "\nThis person is one of my sudo users! " \
                    "Nearly as powerful as my owner - so watch it.."
        
    elif user.id in SUPPORT_USERS:
        text += "\nThis person is one of my support users! " \
                        "Not quite a sudo user, but can still gban you off the map."
        
  
       
    elif user.id in WHITELIST_USERS:
        text += "\nThis person has been whitelisted! " \
                        "That means I'm not allowed to ban/kick them."
       

    


    text += "\n"
    for mod in USER_INFO:
        if mod.__mod_name__ == "Users":
            continue

        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
dispatcher.add_handler(INFO_HANDLER)

import os
import psutil
import random
import time
import datetime
from typing import Optional, List
import re
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from alluka.modules.helper_funcs.chat_status import user_admin, sudo_plus, is_user_admin
from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS, WHITELIST_USERS, BAN_STICKER
from alluka.__main__ import STATS, USER_INFO, TOKEN
from alluka.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from alluka.modules.helper_funcs.extraction import extract_user
from alluka.modules.helper_funcs.filters import CustomFilters
import alluka.modules.sql.users_sql as sql

@run_async
def info(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not message.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    text = (f"<b>Characteristics:</b>\n"
            f"ID: <code>{user.id}</code>\n"
            f"First Name: {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\nLast Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\nUsername: @{html.escape(user.username)}"

    text += f"\nPermanent user link: {mention_html(user.id, 'link')}"

    num_chats = sql.get_user_num_chats(user.id)
    text += f"\nChat count: <code>{num_chats}</code>"

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\nThis user holds the title <b>{custom_title}</b> here."
    except BadRequest:
        pass

   

    if user.id == OWNER_ID:
        text += "\nThis person is my owner - I would never do anything against them!."
        
    elif user.id in DEV_USERS:
        text += "\nThis person is my dev - I would never do anything against them!."
        
    elif user.id in SUDO_USERS:
        text += "\nThis person is one of my sudo users! " \
                    "Nearly as powerful as my owner - so watch it.."
        
    elif user.id in SUPPORT_USERS:
        text += "\nThis person is one of my support users! " \
                        "Not quite a sudo user, but can still gban you off the map."
        
  
       
    elif user.id in WHITELIST_USERS:
        text += "\nThis person has been whitelisted! " \
                        "That means I'm not allowed to ban/kick them."
       

    


    text += "\n"
    for mod in USER_INFO:
        if mod.__mod_name__ == "Users":
            continue

        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
dispatcher.add_handler(INFO_HANDLER)
