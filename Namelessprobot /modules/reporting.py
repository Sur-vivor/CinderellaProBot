import html

from typing import List

from telegram import Bot, Chat, Update, ParseMode
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CommandHandler, RegexHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from cinderella import dispatcher, LOGGER, DEV_USERS, WHITELIST_USERS
from cinderella.modules.helper_funcs.chat_status import user_not_admin, user_admin
from cinderella.modules.log_channel import loggable
from cinderella.modules.sql import reporting_sql as sql

REPORT_GROUP = 5
REPORT_IMMUNE_USERS = DEV_USERS + WHITELIST_USERS


@run_async
@user_admin
def report_setting(bot: Bot, update: Update, args: List[str]):

    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == chat.PRIVATE:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_user_setting(chat.id, True)
                msg.reply_text("Turned on reporting! You'll be notified whenever anyone reports something.")

            elif args[0] in ("no", "off"):
                sql.set_user_setting(chat.id, False)
                msg.reply_text("Turned off reporting! You wont get any reports.")
        else:
            msg.reply_text("Your current report preference is: `{}`".format(sql.user_should_report(chat.id)),
                           parse_mode=ParseMode.MARKDOWN)

    else:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_chat_setting(chat.id, True)
                msg.reply_text("Turned on reporting! Admins who have turned on reports will be notified when /report "
                               "or @admin are called.")

            elif args[0] in ("no", "off"):
                sql.set_chat_setting(chat.id, False)
                msg.reply_text("Turned off reporting! No admins will be notified on /report or @admin.")
        else:
            msg.reply_text("This chat's current setting is: `{}`".format(sql.chat_should_report(chat.id)),
                           parse_mode=ParseMode.MARKDOWN)


@run_async
@user_not_admin
@loggable
def report(bot: Bot, update: Update) -> str:

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if chat and message.reply_to_message and sql.chat_should_report(chat.id):

        reported_user = message.reply_to_message.from_user
        chat_name = chat.title or chat.first or chat.username
        admin_list = chat.get_administrators()
        message = update.effective_message

        if user.id == reported_user.id:
            message.reply_text("You don't seem to be referring to a user.")
            return ""

        if user.id == bot.id:
            message.reply_text("You can't report on me 😏.")
            return ""
        
        if reported_user.id in REPORT_IMMUNE_USERS:
            message.reply_text("You can't report on my whitelist user.")
            return "" 

        if chat.username and chat.type == Chat.SUPERGROUP:

            reported = "{} reported {} to the admins!".format(mention_html(user.id, user.first_name),
                                                              mention_html(reported_user.id, reported_user.first_name))
            
            msg = "<b>{}:</b>" \
                  "\n<b>Reported user:</b> {} (<code>{}</code>)" \
                  "\n<b>Reported by:</b> {} (<code>{}</code>)".format(html.escape(chat.title),
                                                                      mention_html(
                                                                          reported_user.id,
                                                                          reported_user.first_name),
                                                                      reported_user.id,
                                                                      mention_html(user.id,
                                                                                   user.first_name),
                                                                      user.id)
            link = "\n<b>Link:</b> " \
                   "<a href=\"http://telegram.me/{}/{}\">click here</a>".format(chat.username, message.message_id)
            
            
            should_forward = False
        else:
            reported = "{} reported {} to the admins!".format(mention_html(user.id, user.first_name),
                                                              mention_html(reported_user.id, reported_user.first_name))

            msg = "{} is calling for admins in \"{}\"!".format(mention_html(user.id, user.first_name),
                                                               html.escape(chat_name))
            link = ""
            should_forward = True

        message.reply_text(reported, parse_mode=ParseMode.HTML)

        for admin in admin_list:

            if admin.user.is_bot:  # can't message bots
                continue

            if sql.user_should_report(admin.user.id):

                try:
                    bot.send_message(admin.user.id, msg + link, parse_mode=ParseMode.HTML)

                    if should_forward:
                        message.reply_to_message.forward(admin.user.id)

                        if len(message.text.split()) > 1:  # If user is giving a reason, send his message too
                            message.forward(admin.user.id)

                except Unauthorized:
                    pass

                except BadRequest:  # TODO: cleanup exceptions
                    LOGGER.exception("Exception while reporting user")

        return msg

    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    return "This chat is setup to send user reports to admins, via /report and @admin: `{}`".format(
        sql.chat_should_report(chat_id))


def __user_settings__(user_id):
    return "You receive reports from chats you're admin in: `{}`.\nToggle this with /reports in PM.".format(
        sql.user_should_report(user_id))


__help__ = """
 - /report <reason>: reply to a message to report it to admins.
 - @admin: reply to a message to report it to admins.
NOTE: Neither of these will get triggered if used by admins.

*Admin only:*
 - /reports <on/off>: change report setting, or view current status.
   - If done in pm, toggles your status.
   - If in chat, toggles that chat's status.
"""

SETTING_HANDLER = CommandHandler("reports", report_setting, pass_args=True)
REPORT_HANDLER = CommandHandler("report", report, filters=Filters.group)
ADMIN_REPORT_HANDLER = RegexHandler("(?i)@admin(s)?", report)

dispatcher.add_handler(SETTING_HANDLER)
dispatcher.add_handler(REPORT_HANDLER, REPORT_GROUP)
dispatcher.add_handler(ADMIN_REPORT_HANDLER, REPORT_GROUP)

__mod_name__ = "REPORTING"
__handlers__ = [(REPORT_HANDLER, REPORT_GROUP), (ADMIN_REPORT_HANDLER, REPORT_GROUP), (SETTING_HANDLER)]
