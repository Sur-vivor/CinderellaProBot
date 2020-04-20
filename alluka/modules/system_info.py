import speedtest
import psutil
import platform

from datetime import datetime
from platform import python_version, uname
from telegram import Update, Bot, Message, Chat, ParseMode
from telegram.ext import CommandHandler, run_async
from alluka.modules.helper_funcs.chat_status import whitelist_plus, dev_plus
import alluka.modules.helper_funcs.git_api as git
from alluka import dispatcher
from alluka.modules.helper_funcs.filters import CustomFilters


def speed_convert(size):
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@dev_plus
@run_async
def status(bot: Bot, update: Update):
	chat = update.effective_chat
	
	stat = "--- System Status ---\n"
	stat += "alluka Version: `5.5.2`""\n"
	stat += "Python Version: `"+python_version()+"`\n"
	stat += "GitHub API Version: `"+str(git.vercheck())+"`\n"
	#Software Info
	uname = platform.uname()
	softw = "--- Software Information ---\n"
	softw += f"System: `{uname.system}`\n"
	softw += f"Node Name: `{uname.node}`\n"
	softw += f"Release: `{uname.release}`\n"
	softw += f"Version: `{uname.version}`\n"
	softw += f"Machine: `{uname.machine}`\n"
	softw += f"Processor: `{uname.processor}`\n"
	#Boot Time
	boot_time_timestamp = psutil.boot_time()
	bt = datetime.fromtimestamp(boot_time_timestamp)
	softw += f"Boot Time: `{bt.year}`/`{bt.month}`/`{bt.day}`  `{bt.hour}`:`{bt.minute}`:`{bt.second}`\n"
	#CPU Cores
	cpuu = "--- CPU Info ---\n"
	cpuu += "Physical cores:`" + str(psutil.cpu_count(logical=False)) + "`\n"
	cpuu += "Total cores:`" + str(psutil.cpu_count(logical=True)) + "`\n"
	# CPU frequencies
	cpufreq = psutil.cpu_freq()
	cpuu += f"Max Frequency: `{cpufreq.max:.2f}Mhz`\n"
	cpuu += f"Min Frequency: `{cpufreq.min:.2f}Mhz`\n"
	cpuu += f"Current Frequency: `{cpufreq.current:.2f}Mhz`\n"
	# CPU usage
	cpuu += "--- CPU Usage Per Core ---\n"
	for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
	    cpuu += f"Core {i}: `{percentage}%`\n"
	cpuu += f"Total CPU Usage: `{psutil.cpu_percent()}%`\n"
	# RAM Usage
	svmem = psutil.virtual_memory()
	memm = "--- Memory Usage ---\n"
	memm += f"Total: `{get_size(svmem.total)}`\n"
	memm += f"Available: `{get_size(svmem.available)}`\n"
	memm += f"Used: `{get_size(svmem.used)}`\n"
	memm += f"Percentage: `{svmem.percent}%`\n"
	reply = str(stat)+ str(softw) + str(cpuu) + str(memm) + "\n"
	bot.send_message(chat.id, reply, parse_mode=ParseMode.MARKDOWN)


@run_async
def speedtst(update, context):
    chat = update.effective_chat
    del_msg = context.bot.send_message(chat.id, "<code>Running speedtest...</code>",
                               parse_mode=ParseMode.HTML)
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    del_msg.delete()
    update.effective_message.reply_text("<b>SpeedTest Results</b> \n\n"
                                        "<b>Download:</b> "
                                        f"<code>{speed_convert(result['download'])}</code> \n"
                                        "<b>Upload:</b> "
                                        f"<code>{speed_convert(result['upload'])}</code> \n"
                                        "<b>Ping:</b> "
                                        f"<code>{result['ping']}</code> \n"
                                        "<b>ISP:</b> "
                                        f"<code>{result['client']['isp']}</code>",
                                        parse_mode=ParseMode.HTML)


__mod_name__ = "System Info"

STATUS_HANDLER = CommandHandler("system", status, filters=CustomFilters.sudo_filter)
SPEED_HANDLER = CommandHandler("speed", speedtst, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(STATUS_HANDLER)
dispatcher.add_handler(SPEED_HANDLER)
