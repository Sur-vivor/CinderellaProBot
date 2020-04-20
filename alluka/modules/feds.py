import html
from io import BytesIO
from typing import Optional, List
import random
import uuid
import re
import json
import time
import csv
import os
from time import sleep

from future.utils import string_types
from telegram.error import BadRequest, TelegramError, Unauthorized
from telegram import ParseMode, Update, Bot, Chat, User, MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown, mention_html, mention_markdown

from alluka import dispatcher, OWNER_ID, SUDO_USERS, WHITELIST_USERS, MESSAGE_DUMP, LOGGER
from alluka.modules.helper_funcs.handlers import CMD_STARTERS
from alluka.modules.helper_funcs.misc import is_module_loaded, send_to_list
from alluka.modules.helper_funcs.chat_status import is_user_admin
from alluka.modules.helper_funcs.extraction import extract_user, extract_unt_fedban, extract_user_fban
from alluka.modules.helper_funcs.string_handling import markdown_parser
from alluka.modules.disable import DisableAbleCommandHandler

import alluka.modules.sql.feds_sql as sql

from alluka.modules.connection import connected
from alluka.modules.helper_funcs.alternate import send_message

# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo and AyraHikari too
# Federation by MrYacha 2018-2019
# Federation rework by Mizukito Akito 2019
# Federation update v2 by Ayra Hikari 2019
# 
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 22+ hours by @peaktogoo
# Time spended on updating version to v2 = 26+ hours by @AyraHikari
# 
# Total spended for making this features is 68+ hours

# LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")

FBAN_ERRORS = {
	"User is an administrator of the chat",
	"Chat not found",
	"Not enough rights to restrict/unrestrict chat member",
	"User_not_participant",
	"Peer_id_invalid",
	"Group chat was deactivated",
	"Need to be inviter of a user to kick it from a basic group",
	"Chat_admin_required",
	"Only the creator of a basic group can kick group administrators",
	"Channel_private",
	"Not in the chat",
	"Have no rights to send a message"
}

UNFBAN_ERRORS = {
	"User is an administrator of the chat",
	"Chat not found",
	"Not enough rights to restrict/unrestrict chat member",
	"User_not_participant",
	"Method is available for supergroup and channel chats only",
	"Not in the chat",
	"Channel_private",
	"Chat_admin_required",
	"Have no rights to send a message"
}

@run_async
def new_fed(update, context):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	message = update.effective_message
	if chat.type != "private":
		send_message(update.effective_message, "Buat federasi Anda di PM saya, bukan dalam grup.")
		return
	if len(message.text) == 1:
		send_message(update.effective_message, "Tolong tulis nama federasinya!")
		return
	fednam = message.text.split(None, 1)[1]
	if not fednam == '':
		fed_id = str(uuid.uuid4())
		fed_name = fednam
		LOGGER.info(fed_id)
                if user.id == int(OWNER_ID):
			fed_id = fed_name
		
		x = sql.new_fed(user.id, fed_name, fed_id)
		if not x:
			send_message(update.effective_message, "Tidak dapat membuat federasi! Tolong hubungi pembuat saya jika masalah masih berlanjut.")
			return

		send_message(update.effective_message, "*Anda telah berhasil membuat federasi baru!*"\
											"\nNama: `{}`"\
											"\nID: `{}`"
											"\n\nGunakan perintah di bawah ini untuk bergabung dengan federasi:"
											"\n`/joinfed {}`").format(fed_name, fed_id, fed_id), parse_mode=ParseMode.MARKDOWN
		try:
			context.bot.send_message(MESSAGE_DUMP,
				"Federasi <b>{}</b> telah di buat dengan ID: <pre>{}</pre>".format(fed_name, fed_id), parse_mode=ParseMode.HTML)
		except:
			LOGGER.warning("Cannot send a message to MESSAGE_DUMP")
	else:
		send_message(update.effective_message, "Tolong tulis nama federasinya!")




__mod_name__ = "Federations"

__help__ = """
Ah, group management. Everything is fun, until the spammer starts entering your group, and you have to block it. Then you need to start banning more, and more, and it hurts.
But then you have many groups, and you don't want this spammer to be in one of your groups - how can you deal? Do you have to manually block it, in all your groups?
No longer! With Federation, you can make a ban in one chat overlap with all other chats.
You can even designate admin federations, so your trusted admin can ban all the chats you want to protect.
Command:
 - /newfed <fedname>: Create a new Federation with the name given. Users are only allowed to have one Federation. This method can also be used to rename the Federation. (max. 64 characters)
 - /delfed: Delete your Federation, and any information related to it. Will not cancel blocked users.
 - /fedinfo <FedID>: Information about the specified Federation.
 - /joinfed <FedID>: Join the current chat to the Federation. Only chat owners can do this. Every chat can only be in one Federation.
 - /leavefed <FedID>: Leave the Federation given. Only chat owners can do this.
 - /fpromote <user>: Promote Users to give fed admin. Fed owner only.
 - /fdemote <user>: Drops the User from the admin Federation to a normal User. Fed owner only.
 - /fban <user>: Prohibits users from all federations where this chat takes place, and executors have control over.
 - /unfban <user>: Cancel User from all federations where this chat takes place, and that the executor has control over.
 - /setfrules: Arrange Federation rules.
 - /frules: See Federation regulations.
 - /chatfed: See the Federation in the current chat.
 - /fedadmins: Show Federation admin.
 - /fbanlist: Displays all users who are victimized at the Federation at this time.
 - /fednotif <on / off>: Federation settings not in PM when there are users who are fban / unfban.
 - /fedchats: Get all the chats that are connected in the Federation.
 - /importfbans: Reply to the Federation backup message file to import the banned list to the Federation now.
 - /fbanstat: Shows if you/or the user you are replying to or their username is fbanned somewhere or not.
 - /subfed <FedId>: Subscribe your federation to another. Users banned in the subscribed fed will also be banned in this one.
            Note: This does not affect your banlist. You just inherit any bans.
 - /unsubfed <FedId>: Unsubscribes your federation from another. Bans from the other fed will no longer take effect.
 - /fedsubs: List all federations your federation is subscribed to.
 - /setfedlog: Sets the current chat as the federation log. All federation events will be logged here.
 - /unsetfedlog: Unset the federation log. Events will no longer be logged.
 - /fbroadcast:Sent a Message to groups.
 - /myfeds: To know Federations Created by you.
"""

NEW_FED_HANDLER = CommandHandler("newfed", new_fed)


dispatcher.add_handler(NEW_FED_HANDLER)
