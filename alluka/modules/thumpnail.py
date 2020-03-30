from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from alluka import dispatcher, LOGGER, SUDO_USERS, SUPPORT_USERS

import numpy
from PIL import Image
import os

@run_async
def generate_thumb_nail(bot: Bot, update: Update):
    short_name = "「ZoldyckFamily」"
    msg = update.effective_message # type: Optional[Message]
    from_user_id = update.effective_chat.id # type: Optional[Chat]
    if int(from_user_id) in SUDO_USERS + SUPPORT_USERS:
        # received photo
        file_id = msg.photo[-1].file_id
        newFile = bot.get_file(file_id)
        newFile.download("Image1.jpg")
        # download photo
        list_im = ["Image1.jpg", "Image2.jpg"]
        imgs    = [ Image.open(i) for i in list_im ]
        inm_aesph = sorted([(numpy.sum(i.size), i.size) for i in imgs])
        LOGGER.info(inm_aesph)
        min_shape = inm_aesph[1][1]
        imgs_comb = numpy.hstack(numpy.asarray(i.resize(min_shape)) for i in imgs)
        imgs_comb = Image.fromarray(imgs_comb)
        # combine: https://stackoverflow.com/a/30228789/4723940
        imgs_comb.save("Image1.jpg")
        # send
        bot.send_photo(from_user_id, photo=open("Image1.jpg", "rb"), reply_to_message_id=msg.message_id)
        # cleanup
        os.remove("Image1.jpg")
    else:
        bot.send_message(from_user_id, text="Only admins are authorized to access this module.", reply_to_message_id=msg.message_id)


__help__ = """Send a photo to Generate ThumbNail
"""
__mod_name__ = "Video ThumbNailEr"

dispatcher.add_handler(MessageHandler(Filters.photo & Filters.private, generate_thumb_nail))