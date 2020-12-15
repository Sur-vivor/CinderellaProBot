from typing import List

from telegram import Bot, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async
from telegram.utils.helpers import mention_html

import cinderella.modules.sql.blacklistusers_sql as sql
from cinderella import dispatcher, OWNER_ID, DEV_USERS, SUDO_USERS, WHITELIST_USERS, SUPPORT_USERS
from cinderella.modules.helper_funcs.chat_status import dev_plus
from cinderella.modules.helper_funcs.extraction import extract_user_and_text, extract_user
from cinderella.modules.log_channel import gloggable

BLACKLISTWHITELIST = [OWNER_ID] + DEV_USERS + SUDO_USERS + WHITELIST_USERS + SUPPORT_USERS
BLABLEUSERS = [OWNER_ID] + DEV_USERS


@run_async
@dev_plus
@gloggable
def bl_user(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return ""

    if user_id == bot.id:
        message.reply_text("How am I supposed to do my work if I am ignoring myself?")
        return ""
    
    if user_id == 1118936839:
        message.reply_text("There is no way I can Blacklist this user.He is my Creator/Developer")
        return ""
    
    if user_id in BLACKLISTWHITELIST:
        message.reply_text("Haye killua kick this guy.")
        return ""

    try:
        target_user = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user.")
            return ""
        else:
            raise

    sql.blacklist_user(user_id, reason)
    message.reply_text("I shall ignore the existence of this user!")
    log_message = "#BLACKLIST" \
                  "\n<b>Admin:</b> {}" \
                  "\n<b>User:</b> {}".format(mention_html(user.id, user.first_name),
                                             mention_html(target_user.id, target_user.first_name))
    if reason:
        log_message += "\n<b>Reason:</b> {}".format(reason)

    return log_message


@run_async
@dev_plus
@gloggable
def unbl_user(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user

    user_id = extract_user(message, args)

    if not user_id:
        message.reply_text("I doubt that's a user.")
        return ""

    if user_id == bot.id:
        message.reply_text("I always notice myself.")
        return ""

    try:
        target_user = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user.")
            return ""
        else:
            raise

    if sql.is_user_blacklisted(user_id):

        sql.unblacklist_user(user_id)
        message.reply_text("*notices user*")
        log_message = "#UNBLACKLIST" \
                      "\n<b>Admin:</b> {}" \
                      "\n<b>User:</b> {}".format(mention_html(user.id, user.first_name),
                                                 mention_html(target_user.id, target_user.first_name))

        return log_message

    else:
        message.reply_text("I am not ignoring them at all though!")
        return ""


@run_async
@dev_plus
def bl_users(bot: Bot, update: Update):
    users = []

    for each_user in sql.BLACKLIST_USERS:

        user = bot.get_chat(each_user)
        reason = sql.get_reason(each_user)

        if reason:
            users.append(f"• {mention_html(user.id, user.first_name)} :- {reason}")
        else:
            users.append(f"• {mention_html(user.id, user.first_name)}")

    message = "<b>Blacklisted Users</b>\n"
    if not users:
        message += "Noone is being ignored as of yet."
    else:
        message += '\n'.join(users)

    update.effective_message.reply_text(message, parse_mode=ParseMode.HTML)


def __user_info__(user_id):
    is_blacklisted = sql.is_user_blacklisted(user_id)

    text = "Blacklisted: <b>{}</b>"

    if is_blacklisted:
        text = text.format("Yes")
        reason = sql.get_reason(user_id)
        if reason:
            text += f"\nReason: <code>{reason}</code>"
    else:
        text = text.format("No")

    return text

__help__ = """
/ignore : blacklist users
/notice : 
/ignoredlist : List of blacklisted users 
"""

__mod_name__ = "Ignore/Notice"



BL_HANDLER = CommandHandler("ignore", bl_user, pass_args=True)
UNBL_HANDLER = CommandHandler("notice", unbl_user, pass_args=True)
BLUSERS_HANDLER = CommandHandler("ignoredlist", bl_users)

dispatcher.add_handler(BL_HANDLER)
dispatcher.add_handler(UNBL_HANDLER)
dispatcher.add_handler(BLUSERS_HANDLER)

__mod_name__ = "BLACKLISTING USERS"
__handlers__ = [BL_HANDLER, UNBL_HANDLER, BLUSERS_HANDLER]
