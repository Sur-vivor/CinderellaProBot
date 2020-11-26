import asyncio
import time

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from cinderella import DEV_USERS, SUDO_USERS, client

# Check if user has admin rights


async def is_administrator(user_id: int, message):
    admin = False
    async for user in client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SUDO_USERS or user_id in DEV_USERS:
            admin = True
            break
    return admin


@client.on(events.NewMessage(pattern="^/purge"))
async def purge(event):
    start = time.perf_counter_ns()
    chat = event.chat_id
    msgs = []

    if not await is_administrator(user_id=event.from_id, message=event):
        await event.reply("You're not an admin!")
        return

    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to a message to select where to start purging from.")
        return

    try:
        msg_id = msg.id
        count = 0
        end = time.perf_counter_ns()
        time_taken = (end - start) / (10 ** 6)  # ns to ms
        timep = "{:.2f}".format(time_taken)
        to_delete = event.message.id - 1
        await event.client.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []

        await event.client.delete_messages(chat, msgs)
        del_res = await event.client.send_message(
            event.chat_id, f"Purged {count} messages.\nin {timep}ms"
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = "Failed to delete messages.\n"
        text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
        del_res = await event.respond(text, parse_mode="md")
        await asyncio.sleep(7)
        await del_res.delete()


@client.on(events.NewMessage(pattern="^/del$"))
async def delete_msg(event):

    if not await is_administrator(user_id=event.from_id, message=event):
        await event.reply("You're not an admin!")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    remove = [msg, to_delete]
    await event.client.delete_messages(chat, remove)

__help__ = """
*Admin only:*
 - /del: deletes the message you replied to
 - /purge: deletes all messages between this and the replied to message.
 - /purge <integer X>: deletes the replied message, and X messages following it if replied to a message.
 - /purge <integer X>: deletes the number of messages starting from bottom. (Counts manaully deleted messages too)
"""
__mod_name__ = "PURGE"
