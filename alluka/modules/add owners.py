import html

from typing import List

from telegram import Update, Bot
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async

from alluka import dispatcher, SUDO_USERS, OWNER_USERNAME, WHITELIST_USERS, SUPPORT_USERS, OWNER_ID
from alluka.modules.helper_funcs.extraction import extract_user
from alluka.modules.helper_funcs.chat_status import bot_admin


@bot_admin
@run_async
def addsudo(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    banner = update.effective_user
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer a user first....")
        return ""
        
    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! No need add him to Sudo User list!")
        return ""
        
    if int(user_id) in SUDO_USERS:
        message.reply_text("Buddy this user is already a Sudo user.")
        return ""
    
    with open("sudo_users.txt","a") as file:
        file.write(str(user_id) + "\n")
    
    SUDO_USERS.append(user_id)
    message.reply_text("Succefully Added To Sudo List!")
        
    return ""

@bot_admin
@run_async
def rsudo(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer the user first.")
        return ""

    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! I won't remove him from Sudo User list!")
        return ""
    
    if user_id not in SUDO_USERS:
        message.reply_text("{} is not a Sudo User".format(user_id))
        return ""

    users = [line.rstrip('\n') for line in open("sudo_users.txt")]

    with open("sudo_users.txt","w") as file:
        for user in users:
            if not int(user) == user_id:
                file.write(str(user) + "\n")

    SUDO_USERS.remove(user_id)
    message.reply_text("Yep Succefully removed from Sudo List!")
    
    return ""

@bot_admin
@run_async
def addsupport(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    banner = update.effective_user
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer a user first....")
        return ""
        
    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! No need add him to Support User list!")
        return ""
        
    if int(user_id) in SUPPORT_USERS:
        message.reply_text("Buddy this user is already a Support User.")
        return ""
    
    with open("support_users.txt","a") as file:
        file.write(str(user_id) + "\n")
    
    SUPPORT_USERS.append(user_id)
    message.reply_text("Succefully Added To Support List!")
        
    return ""

@bot_admin
@run_async
def rsupport(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer the user first.")
        return ""

    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! I won't remove him from Support User list!")
        return ""
    
    if user_id not in SUPPORT_USERS:
        message.reply_text("{} is not a Support user".format(user_id))
        return ""

    users = [line.rstrip('\n') for line in open("support_users.txt")]

    with open("support_users.txt","w") as file:
        for user in users:
            if not int(user) == user_id:
                file.write(str(user) + "\n")

    SUPPORT_USERS.remove(user_id)
    message.reply_text("Yep Succefully removed from Support User List!")
    
    return ""

@bot_admin
@run_async
def addwhitelist(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    banner = update.effective_user
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer a user first....")
        return ""
        
    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! No need add him to Whitelist!")
        return ""
        
    if int(user_id) in WHITELIST_USERS:
        message.reply_text("Buddy this user is already a Whitelist user.")
        return ""
    
    with open("whitelist_users.txt","a") as file:
        file.write(str(user_id) + "\n")
    
    WHITELIST_USERS.append(user_id)
    message.reply_text("Succefully Added To Whitelist!")
        
    return ""

@bot_admin
@run_async
def rwhitelist(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    
    if not user_id:
        message.reply_text("Refer the user first.")
        return ""

    if int(user_id) == OWNER_ID:
        message.reply_text("The specified user is my owner! I won't remove him from Whitelist!")
        return ""
    
    if user_id not in WHITELIST_USERS:
        message.reply_text("{} is not a Whitelist user".format(user_id))
        return ""

    users = [line.rstrip('\n') for line in open("whitelist_users.txt")]

    with open("whitelist_users.txt","w") as file:
        for user in users:
            if not int(user) == user_id:
                file.write(str(user) + "\n")

    WHITELIST_USERS.remove(user_id)
    message.reply_text("Yep Succefully removed from Whitelist!")
    
    return ""


__help__ = """
*Bot owner only:*

 - /addsudo: promotes the user to Sudo User
 - /rsudo: demotes the user from Sudo User

 - /addsupport: promotes the user to Support User
 - /rsupport: demotes the user from Support User

 - /addwhitelist: promotes the user to Whitelist User
 - /rwhitelist: demotes the user from Whitelist User
"""

__mod_name__ = "Dev Promoter"

addsudo_HANDLER = CommandHandler("addsudo", addsudo, pass_args=True, filters=Filters.user(OWNER_ID))
rsudo_HANDLER = CommandHandler("rsudo", rsudo, pass_args=True, filters=Filters.user(OWNER_ID))
addsupport_HANDLER = CommandHandler("addsupport", addsupport, pass_args=True, filters=Filters.user(OWNER_ID))
rsupport_HANDLER = CommandHandler("rsupport", rsupport, pass_args=True, filters=Filters.user(OWNER_ID))
addwhitelist_HANDLER = CommandHandler("addwhitelist", addwhitelist, pass_args=True, filters=Filters.user(OWNER_ID))
rwhitelist_HANDLER = CommandHandler("rwhitelist", rwhitelist, pass_args=True, filters=Filters.user(OWNER_ID))


dispatcher.add_handler(addsudo_HANDLER)
dispatcher.add_handler(rsudo_HANDLER)
dispatcher.add_handler(addsupport_HANDLER)
dispatcher.add_handler(rsupport_HANDLER)
dispatcher.add_handler(addwhitelist_HANDLER)
dispatcher.add_handler(rwhitelist_HANDLER)
