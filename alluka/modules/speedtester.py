from typing import List

import requests
import speedtest
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from telegram.ext import run_async, CommandHandler
from alluka import dispatcher
from alluka.modules.disable import DisableAbleCommandHandler
from alluka.modules.helper_funcs.chat_status import dev_plus
from alluka import dispatcher, WHITELIST_USERS, SUPPORT_USERS, SUDO_USERS, DEV_USERS, OWNER_ID
from alluka.modules.helper_funcs.chat_status import whitelist_plus, dev_plus

def paste(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text

    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]

    else:
        message.reply_text("What am I supposed to do with this?")
        return

    key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')

    url = f'https://nekobin.com/{key}'

    reply_text = f'Nekofied to *Nekobin* : {url}'

    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
@whitelist_plus
def speedtestxyz(bot: Bot, update: Update):
    s = speedtest.Speedtest()
    msg = update.effective_message.reply_text("Doing SpeedTest.... ")
    s.get_best_server()
    s.download()
    s.upload()
    speedtest_image = s.results.share()
    update.effective_message.reply_photo(photo=speedtest_image, caption='Done!')
    msg.delete()


__mod_name__ = "Paste bin"
__help__ = """
 - /paste

"""

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, pass_args=True)
SpeedTest_handler = CommandHandler("speedtest", speedtestxyz)
dispatcher.add_handler(SpeedTest_handler)
dispatcher.add_handler(PASTE_HANDLER)
