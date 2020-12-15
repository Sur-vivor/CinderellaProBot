import speedtest
import psutil
import platform
from datetime import datetime
from platform import python_version, uname
from telegram import Update, Bot, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import run_async, CallbackQueryHandler, CommandHandler

from cinderella import dispatcher, DEV_USERS, VERSION
from cinderella.modules.disable import DisableAbleCommandHandler
from cinderella.modules.helper_funcs.chat_status import dev_plus
import cinderella.modules.helper_funcs.git_api as git
from cinderella.modules.helper_funcs.filters import CustomFilters

def convert(speed):
    return round(int(speed)/1048576, 2)


@dev_plus
@run_async
def speedtestxyz(bot: Bot, update: Update):
    buttons = [
        [InlineKeyboardButton("🖼Image", callback_data="speedtest_image"), InlineKeyboardButton("📝Text", callback_data="speedtest_text")]
    ]
    update.effective_message.reply_text("Select SpeedTest Mode",
                                        reply_markup=InlineKeyboardMarkup(buttons))


@run_async
def speedtestxyz_callback(bot: Bot, update: Update):
    query = update.callback_query

    if query.from_user.id in DEV_USERS:
        msg = update.effective_message.edit_text('Runing a speedtest....') 
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = '*SpeedTest Results*'

        if query.data == 'speedtest_image':
            speedtest_image = speed.results.share()
            update.effective_message.reply_photo(photo=speedtest_image, caption=replymsg)
            msg.delete()

        elif query.data == 'speedtest_text':
            result = speed.results.dict()
            replymsg += f"\n\n*Download:* `{convert(result['download'])}Mb/s`\n*Upload:* `{convert(result['upload'])}Mb/s`\n*Ping:* `{result['ping']}`\n*ISP:* `{result['client']['isp']}`"
            update.effective_message.edit_text(replymsg, parse_mode=ParseMode.MARKDOWN)
    else:
        query.answer("You are required to join Heroes Association to use this command.")

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
	stat += f"Cinderella Version: `{VERSION}`""\n"
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

__help__ = """
- /system : To know System status
- /speed or - /speedtest: To find Speed
"""
	
SPEED_TEST_HANDLER = DisableAbleCommandHandler(["speedtest","speed"], speedtestxyz, filters=CustomFilters.sudo_filter)
SPEED_TEST_CALLBACKHANDLER = CallbackQueryHandler(speedtestxyz_callback, pattern='speedtest_.*')
STATUS_HANDLER = CommandHandler("system", status, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(SPEED_TEST_HANDLER)
dispatcher.add_handler(SPEED_TEST_CALLBACKHANDLER)
dispatcher.add_handler(STATUS_HANDLER)

__mod_name__ = "SYSTEM INFO"
__command_list__ = ["speedtest"]
__handlers__ = [SPEED_TEST_HANDLER, SPEED_TEST_CALLBACKHANDLER]
