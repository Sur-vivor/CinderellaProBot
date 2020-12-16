from julia import SUDO_USERS, tbot, OWNER_ID
from julia.events import register
from telethon.tl.types import ChatBannedRights
from telethon.tl import functions
from telethon.tl import types
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from pymongo import MongoClient
from julia import MONGO_DB_URI

G_BAN_LOGGER_GROUP = "@MissJuliaRobotGbans"
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
gbanned = db.gban


def get_reason(id):
    return gbanned.find_one({"user": id})


@register(pattern="^/gban(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.sender_id in SUDO_USERS:
       pass
    elif event.sender_id == OWNER_ID:
       pass
    else:
       return
    reason = event.pattern_match.group(1)
    if not reason:
      reason = "No reason given"
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_sender_id = r.sender_id

    chats = gbanned.find({})

    for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.update_one({"_id": to_check["_id"], "bannerid": to_check["bannerid"], "user": to_check["user"], "reason": to_check["reason"]}, {
                               "$set": {"reason": reason}})
            await event.reply("This user is already gbanned, I am updating the reason of the gban with your reason.")
            await event.client.send_message(
                G_BAN_LOGGER_GROUP,
                "**GLOBAL BAN REASON UPDATE**\n\n**PERMALINK:** [user](tg://user?id={})\n**REASON:** `{}`".format(r_sender_id, reason))
            return

    gbanned.insert_one({"bannerid": event.sender_id, "user": r_sender_id, "reason": reason})

    await event.client.send_message(
            G_BAN_LOGGER_GROUP,
            "**NEW GLOBAL BAN**\n\n**PERMALINK:** [user](tg://user?id={})\n**REASON:** `{}`".format(
                r_sender_id, reason)
        )
    await event.reply("Gbanned Successfully !")


@register(pattern="^/ungban(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.sender_id in SUDO_USERS:
       pass
    elif event.sender_id == OWNER_ID:
       pass
    else:
       return
    reason = event.pattern_match.group(1)
    if not reason:
      reason = "No reason given"
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_sender_id = r.sender_id

    chats = gbanned.find({})

    for c in chats:
        if r_sender_id == c["user"]:
            to_check = get_reason(id=r_sender_id)
            gbanned.delete_one({"user": r_sender_id})
            await event.client.send_message(
                  G_BAN_LOGGER_GROUP,
                  "**REMOVAL OF GLOBAN BAN**\n\n**PERMALINK:** [user](tg://user?id={})\n**REASON:** `{}`".format(
                      r_sender_id, reason)
               )
            await event.reply("Ungbanned Successfully !")
            return
    await event.reply("Is that user even gbanned ?")


@tbot.on(events.ChatAction())
async def join_ban(event):
    if event.user_joined:
      try:
        user = await event.get_user()
        chat = await event.get_chat()
        to_check = get_reason(id=user.id)
        reason = to_check["reason"]
        bannerid = to_check["bannerid"]
        await tbot(EditBannedRequest(chat.id, user.id, BANNED_RIGHTS))
        await event.reply("This user is gbanned and has been removed !\n\n**Gbanned By**: `{}`\n**Reason**: `{}`".format(bannerid, reason))
      except Exception as e:
        print(e)
        return

@tbot.on(events.NewMessage(pattern=None))
async def type_ban(event):
   chats=gbanned.find({})
   for c in chats:
       if event.sender_id == c["user"]:
          try:
            to_check = get_reason(id=event.sender_id)
            reason = to_check["reason"]
            bannerid = to_check["bannerid"]
            await tbot(EditBannedRequest(event.chat_id, event.sender_id, BANNED_RIGHTS))
            await event.reply("This user is gbanned and has been removed !\n\n**Gbanned By**: `{}`\n**Reason**: `{}`".format(bannerid, reason))
          except Exception as e:
             print(e)
             return
