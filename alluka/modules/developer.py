import subprocess
import os
import sys

from typing import List
from time import sleep

from telegram import Bot, Update, TelegramError
from telegram.ext import CommandHandler, run_async

from alluka import dispatcher
from alluka.modules.helper_funcs.chat_status import dev_plus

@run_async
@dev_plus
def leave(bot: Bot, update: Update, args: List[str]):

    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("I left that chat!.")
        except TelegramError:
            update.effective_message.reply_text("I could not leave that group")
    else:
        update.effective_message.reply_text("Send a valid chat ID") 


@run_async
@dev_plus
def gitpull(bot: Bot, update: Update):

    sent_msg = update.effective_message.reply_text("Pulling all changes from remote and then attempting to restart.")
    subprocess.Popen('git pull', stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)
    
    sent_msg.edit_text("Restarted.")
    
    os.system('restart.bat')
    os.execv('start.bat', sys.argv)


@run_async
@dev_plus
def restart(bot: Bot, update: Update):

    update.effective_message.reply_text("Starting a new instance and shutting down this one")

    os.system('restart.bat')
    os.execv('start.bat', sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, pass_args = True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("restart", restart)

dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER]
