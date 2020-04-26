import html
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
def info(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat

    if user_id:
        user = context.bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text("I can't extract a user from this.")
        return

    else:
        return

    del_msg = msg.reply_text("Hold tight while I steal some data from <b>FBI Database</b>...", parse_mode=ParseMode.HTML)

    text = "<b>USER INFO</b>:" \
           "\n\nID: <code>{}</code>" \
           "\nFirst Name: {}".format(user.id, html.escape(user.first_name))

    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))

    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))

    text += "\nPermanent user link: {}".format(mention_html(user.id, "link"))

    text += "\nNumber of profile pics: {}".format(context.bot.get_user_profile_photos(user.id).total_count)

    if user.id == OWNER_ID:
        text += "\n\nAye this guy is my owner - I would never do anything against him!"

    elif user.id in SUDO_USERS:
        text += "\n\nThis person is one of my sudo users! " \
                    "Nearly as powerful as my owner - so watch it."

    elif user.id in SUPPORT_USERS:
        text += "\n\nThis person is one of my support users! " \
                    "Not quite a sudo user, but can still gban you off the map."

    elif user.id in WHITELIST_USERS:
        text += "\n\nThis person has been whitelisted! " \
                    "That means I'm not allowed to ban/kick them."

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\n\nThis user has custom title <b>{custom_title}</b> in this chat."
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    try:
        profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
        context.bot.sendChatAction(chat.id, "upload_photo")
        context.bot.send_photo(chat.id, photo=profile, caption=(text), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        del_msg.delete()
    except IndexError:
        context.bot.sendChatAction(chat.id, "typing")
        msg.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        del_msg.delete()
          
    
INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
dispatcher.add_handler(INFO_HANDLER)
