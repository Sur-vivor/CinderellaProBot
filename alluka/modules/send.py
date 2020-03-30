from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER
from alluka import dispatcher
from telegram.ext import CommandHandler, run_async, Filters
from requests import get
from alluka.modules.helper_funcs.filters import CustomFilters

@run_async
def send(bot: Bot, update: Update):
  chat = update.effective_chat
  message = update.effective_message
  
  text = message.text[len('/send '):]
  
  reply_text = f'{text}'
  
  bot.send_message(chat.id, reply_text, parse_mode=ParseMode.MARKDOWN)
  update.effective_message.delete()

  
  
send_handler = CommandHandler("send", send, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(send_handler)
