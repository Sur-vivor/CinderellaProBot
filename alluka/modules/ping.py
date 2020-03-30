import time
import requests

from typing import List

from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

from alluka import dispatcher, StartTime
from alluka.modules.disable import DisableAbleCommandHandler


sites_list = {
    "Telegram" : "https://api.telegram.org",
    "Anilchauhanxda.github.io" : "https://anilchauhanxda.github.io",
    "Mitshuhataki.github.io" : "https://mitshuhataki.github.io",
    "Parawalls.github.io" : "https://parawalls.github.io"
}

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


def ping_func(to_ping: List[str]) -> List[str]:

    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = str(round((end_time - start_time), 2)) + "s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping is "Mitshuhataki.github.io" or each_ping is "Parawalls.github.io":
            pinged_site = f'<a href="{sites_list[each_ping]}">{each_ping}</a>'
            ping_time = f"<code>{ping_time} (Status: {r.status_code})</code>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@run_async
def ping(bot: Bot, update: Update):

    telegram_ping = ping_func(["Telegram"])[0].split(": ", 1)[1]
    uptime = get_readable_time((time.time() - StartTime))

    reply_msg = "PONG!!\n<b>Time Taken:</b> <code>{}</code>" \
                "\n<b>Service uptime:</b> <code>{}</code>".format(telegram_ping, uptime)

    update.effective_message.reply_text(reply_msg, parse_mode=ParseMode.HTML)


__help__ = """
 - /ping - get ping time of bot to telegram server
 
"""

PING_HANDLER = DisableAbleCommandHandler("ping", ping)


dispatcher.add_handler(PING_HANDLER)


__mod_name__ = "Ping"
__command_list__ = ["ping"]
__handlers__ = [PING_HANDLER]
