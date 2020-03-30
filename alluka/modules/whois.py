import html
import json
import os
import psutil
import random
import time
import datetime
from typing import Optional, List
import re
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from alluka.modules.helper_funcs.chat_status import user_admin, sudo_plus, is_user_admin
from alluka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS, WHITELIST_USERS, BAN_STICKER
from alluka import dispatcher, ALLUKA, HISOKA, KITE, GING, SHIZUKU, SILVA, GON, ILLUMI_ZOLDYCK, LEORIO, BISCUIT, CHROLLO, KILLUA, MERUEM
from alluka.__main__ import STATS, USER_INFO, TOKEN
from alluka.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from alluka.modules.helper_funcs.extraction import extract_user
from alluka.modules.helper_funcs.filters import CustomFilters


@run_async
def info(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    chat = update.effective_chat # type: Optional[Chat]
    user_id = extract_user(update.effective_message, args)

    

    if user_id:
        user = bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text("I can't extract a user from this.")
        return

    else:
        return

    text = "<b>Characteristics:</b>" \
           "\nID: <code>{}</code>" \
           "\nFirst Name: {}".format(user.id, html.escape(user.first_name))
   

    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))

    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))

    text += "\nPermanent user link: {}".format(mention_html(user.id, "link"))



    disaster_level_present = False
    if user.id == OWNER_ID:
        text += "\n\nMoi creator!!💙 If you wanna know more about him visit his personal website anilchauhanxda.github.io"
        img = "https://telegra.ph/file/633307eb7b142003c096c.jpg"
        disaster_level_present = True
    elif user.id in HISOKA:
        text += "\n\nHe is Hisoka Morow (ヒソカ゠モロウ, Hisoka Morou) is a Hunter and former member #4 of the Phantom Troupe; his physical strength ranked third in the group. He is always in search for strong opponents, and would spare those who have great potential, such as Gon and Killua in order for them to get strong enough to actually challenge him. He originally served as the primary antagonist of the Hunter Exam arc and a secondary one of the Heavens Arena arc, before becoming a supporting character during the Yorknew City arc and Greed Island arc. During the 13th Hunter Chairman Election arc, he briefly reprises his role as a secondary antagonist.\n <i>'My greatest pleasure comes when such people crumple to their knees and I look down upon their disbelieving faces as their plans fail.♥'</i>"
        img = "https://telegra.ph/file/4aee5cfe2ba8a3fa503d0.jpg"
        disaster_level_present = True
    elif user.id in GING:
        text += "\n\nHe is Ging Freecss (ジン゠フリークス, Jin Furīkusu) is the father of Gon Freecss. He is a Double-Star Ruins Hunter (though he can apply for a Triple-Star License),and a former Zodiac with the codename 'Boar' (亥, I). Finding Ging was Gon's motivation for becoming a Hunter. \n <i>'I'm enjoying the journey. So if your destination is the same as mine, enjoy the side trips. A lot. Something more important than the thing you're hunting could be right there by the side of the road.'</i>"
        img = "https://telegra.ph/file/22a1c264865bd07af7556.png"
        disaster_level_present = True
    elif user.id in SHIZUKU:
        text+= "\n\nHe is <b>Shizuku Murasaki</b> (シズク゠ムラサキ, Shizuku Murasaki) is member #8 of the Phantom Troupe, an infamous gang of thieves with class A bounties. Her physical strength ranks twelfth in the group. \n<i>'Breaking the rules means rejecting the Spiders, and Chrollo, too. That I never want to do.'</i> "
        img = "https://telegra.ph/file/31fcbda7396fb94d7fc62.png"
        disaster_level_present = True
    elif user.id in SILVA:
        text += "\n\nHe is my father Silva Zoldyck (シルバ゠ゾルディック, Shiruba Zorudikku) is the current head of the Zoldyck Family and the father of Killua.\n<i>'Never overreach your limits...! Make your move only when you're 100% positive you can make the kill. Otherwise, bide your time...!! It's foolish to show your hand when the odds are against you.'</i>"
        img = "https://telegra.ph/file/37bf67a10d77b9661bec1.png"
        disaster_level_present = True

    elif user.id in GON:
        text += "\n\nHe is Gon Freecss (ゴン゠フリークス, Gon Furīkusu) is a Rookie Hunter and the son of Ging Freecss. Finding his father is Gon's motivation in becoming a Hunter\n<i>'I can't stand being on the losing end forever!! '</i>"
        img = "https://telegra.ph/file/8f5d722e7f29da3226f03.png"
        disaster_level_present = True
   
    elif user.id in ILLUMI_ZOLDYCK:
        text += "\n\nHe is <b>Illumi Zoldyck</b> (イルミ゠ゾルディック, Irumi Zorudikku) is the eldest child of Silva and Kikyo Zoldyck. During the 287th Hunter Exam, he appeared under the guise of Gittarackur (ギタラクル, Gitarakuru). At Hisoka's request, Illumi joins the Phantom Troupe as Uvogin's replacement, becoming Troupe member #11. He served as a secondary antagonist of the Hunter Exam arc and the primary one of the 13th Hunter Chairman Election arc. \n<i>'Now I can tell you, that you would not make a good Hunter. Your calling is as an assassin. There's no fire in you, just darkness. It sustains you, drains you of any desire. Your only joy is in causing death, and even that is fleeting. That is how Dad and I molded you'</i>"
        img = "https://telegra.ph/file/689f2d3b1f5f2ae4d3005.png"
        disaster_level_present = True

    elif user.id in LEORIO:
        text += "\n\nHe is <b>Leorio Paradinight</b> (レオリオ゠パラディナｲﾄ, Reorio Paradinaito) is a Rookie Hunter and a member of the Zodiacs with the codename 'Boar' (亥, I). He is currently a medical student, with a goal to become a doctor.\n <i>'I'm a simple guy. Figured I'd become a doctor... so I could cure some kid with the same disease, tell his parents they owed me nothing! Me... A doctor! Now there's a joke!! Do you know how much it costs to even try to become a doctor? The mind boggles!! It's always about money! Always!! That's why I want it!'</i>"
        img = "https://telegra.ph/file/16cc60c94d7ff535e3957.png"
        disaster_level_present = True
    elif user.id in BISCUIT:
        text += "\n\nHe is <b>Biscuit Krueger</b> (ビスケット゠クルーガー, Bisuketto Kurūgā) is a Double-Star Stone Hunter[2] that enlisted in clearing the video game Greed Island following the auction for the game in Yorknew City. She prefers to be called 'Bisky' (ビスケ, Bisuke).\n <i>'After 50 years of lying through my teeth, I can tell whether someone's telling the truth.'</i>"
        img = "https://telegra.ph/file/f3439e1ea77e6f4a2d6bb.png"
        disaster_level_present = True
    elif user.id in CHROLLO:
        text += "\n\nHe is <b>Chrollo Lucilfer</b> (クロロ゠ルシルフル, Kuroro Rushirufuru) is the founder and leader and member #0[4] of the Phantom Troupe, an infamous gang of thieves with class A bounties. His physical strength ranks seventh in the group.\n <i>'Making the abilities yours while exploring the darkness within the soul of the original owner... that's the true pleasure of 'Skill Hunter'.'</i>"
        img = "https://telegra.ph/file/d4888fcbdeb3261a2a9cf.png"
        disaster_level_present = True
    elif user.id in KILLUA:
        text += "\n\nHe is my elder brother <b>Killua Zoldyck </b> (キルア゠ゾルディック, Kirua Zorudikku) is the third child of Silva and Kikyo Zoldyck and the heir of the Zoldyck Family, until he runs away from home and becomes a Rookie Hunter. He is the best friend of Gon Freecss, and is currently travelling with Alluka Zoldyck. \n <i>'I'm so tired of killing... I just want to be a kid. Hanging out, doing stuff with Gon. That's it'.'</i>"
        img = "https://telegra.ph/file/335efcdd8ffb462371582.png"
        disaster_level_present = True
        
    elif user.id in MERUEM:
        text += "\n\nHe is <b>Meruem  </b>(メルエム, Meruemu) was the most powerful offspring of the Chimera Ant Queen. He was known as the 'King' (王, Ō) of the Chimera Ants, and served as the main antagonist of the Chimera Ant arc.  \n <i>'Who am I? Why am I here? A king with no name. A borrowed castle. My subjects are mindless drones. If this is the mandate of Heaven I have been given... I fear... I fear nothing... except the tedium that it will bring!!!'.'</i>"
        img = "https://telegra.ph/file/348ae7fcba0116a9a4314.jpg"
        disaster_level_present = True
      
    elif user.id in KITE:
        text += """\n\nHe is <b>Kite (カイト)</b>, He is the very first Hunter introduced in the story. He is a disciple of Ging Freecss, Gon's father. After saving Gon from a foxbear on Whale Island, Kite revealed to him the truth about his father. Before he took his leave, Kite left Ging's Hunter License in Gon's hands.
After leaving Greed Island, Gon runs into Kite again, while he is in the middle of a zoological survey, searching for new species, in the country of Kakin. At the time, he was leading a team of young would-be Hunters, seven children named Banana Kavaro, Lin Koshi, Monta Yuras, Podungo Lapoy, Spinner Clow, and Stick Dinner."""
        img = "https://telegra.ph/file/520c4b38b71f82e312f5b.png"
        disaster_level_present = True
    
    

      
   

     
     

    if disaster_level_present:
        
        update.effective_message.reply_photo(img, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return
    user_member = chat.get_member(user.id)
    if user_member.status == 'administrator':
        result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
        result = result.json()["result"]
        if "custom_title" in result.keys():
            custom_title = result['custom_title']
            text += f"\n\nThis user holds the title <b>{custom_title}</b> here."

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)



INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
dispatcher.add_handler(INFO_HANDLER)
