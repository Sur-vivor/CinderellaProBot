# AI module using Intellivoid's Coffeehouse API by @TheRealPhoenix

from time import time, sleep
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError

from telegram import Message, Chat, User, Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, run_async

from cinderella import dispatcher, LYDIA_API, OWNER_ID
import cinderella.modules.sql.lydia_sql as sql
from cinderella.modules.helper_funcs.filters import CustomFilters


CoffeeHouseAPI = API(LYDIA_API)
api_client = LydiaAI(CoffeeHouseAPI)


@run_async
def add_chat(bot: Bot, update: Update):
    global api_client
    chat_id = update.effective_chat.id
    msg = update.effective_message
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        sql.set_ses(chat_id, ses_id, expires)
        msg.reply_text("Lydia successfully enabled for this chat!")
    else:
        msg.reply_text("Lydia is already enabled for this chat!")
        
        
@run_async
def remove_chat(bot: Bot, update: Update):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        msg.reply_text("Lydia isn't enabled here in the first place!")
    else:
        sql.rem_chat(chat_id)
        msg.reply_text("Lydia disabled successfully!")
        
        
def check_message(bot: Bot, message):
    reply_msg = message.reply_to_message
    if message.text.lower() == "cinderella":
        return True
    if reply_msg:
        if reply_msg.from_user.id == bot.get_me().id:
            return True
    else:
        return False
                
        
@run_async
def lydia(bot: Bot, update: Update):
    global api_client
    msg = update.effective_message
    chat_id = update.effective_chat.id
    is_chat = sql.is_chat(chat_id)
    if not is_chat:
        return
    if msg.text and not msg.document:
        if not check_message(bot, msg):
            return
        sesh, exp = sql.get_ses(chat_id)
        query = msg.text
        try:
            if int(exp) < time():
                ses = api_client.create_session()
                ses_id = str(ses.id)
                expires = str(ses.expires)
                sql.set_ses(chat_id, ses_id, expires)
                sesh, exp = sql.get_ses(chat_id)
        except ValueError:
            pass
        try:
            bot.send_chat_action(chat_id, action='typing')
            rep = api_client.think_thought(sesh, query)
            sleep(0.3)
            msg.reply_text(rep, timeout=60)
        except CFError as e:
            bot.send_message(OWNER_ID, f"lydia error: {e} occurred in {chat_id}!")
                    

__mod_name__ = "LYDIA/CHATBOT"

__help__ = """
Commands
 - /elydia : Enables Lydia mode in the chat.
 - /dlydia  : Disables Lydia mode in the chat.
 
 
"""
                  
ADD_CHAT_HANDLER = CommandHandler("elydia", add_chat, filters=CustomFilters.dev_filter)
REMOVE_CHAT_HANDLER = CommandHandler("dlydia", remove_chat, filters=CustomFilters.dev_filter)
LYDIA_HANDLER = MessageHandler(Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                                  & ~Filters.regex(r"^s\/")), lydia)
# Filters for ignoring #note messages, !commands and sed.

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(REMOVE_CHAT_HANDLER)
dispatcher.add_handler(LYDIA_HANDLER)
