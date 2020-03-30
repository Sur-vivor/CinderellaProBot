from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from alluka.modules.disable import DisableAbleCommandHandler
from alluka import dispatcher

from requests import get

@run_async
def ud(bot: Bot, update: Update):
  message = update.effective_message
  text = message.text[len('/familylist '):]
  
  sunnyimg = "https://telegra.ph/file/4aee5cfe2ba8a3fa503d0.jpg"
  sunny = """[Sunny ZoldyckFamily」](https://telegram.dog/medevilofmelodies) as Hisoka Morow.\n To get more about him do `!info @medevilofmelodies`"""

  bhavikimg = "https://telegra.ph/file/22a1c264865bd07af7556.png"
  bhavik = """[Inhuman ZoldyckFamily」](https://telegram.dog/artificialHuman) as Ging Freecss.\n To get more about him do `!info @artificialHuman`"""

  drakxtorimg = "https://telegra.ph/file/335efcdd8ffb462371582.png"
  drakxtor = """[Muzammil ZoldyckFamily」](https://telegram.dog/drakxtor) as elder bro Killua Zoldyck.\n To get more about him do `!info @drakxtor`"""

  alokimg = "https://telegra.ph/file/31fcbda7396fb94d7fc62.png"
  alok = """[Alok ZoldyckFamily」](https://telegram.dog/FirefistX45) as Shizuku Murasaki.\n To get more about him do `!info @FirefistX45`"""

  neelimg = "https://telegra.ph/file/520c4b38b71f82e312f5b.png"
  neel = """[Neel ZoldyckFamily」](https://telegram.dog/spookyenvy) as Kite.\n To get more about him do `!info @spookyenvy`"""

  kiritoimg = "https://telegra.ph/file/f3439e1ea77e6f4a2d6bb.png"
  kirito = """[Kirito ZoldyckFamily」](https://telegram.dog/Kirito_Kiri) as Biscuit Krueger.\n To get more about him do `!info @Kirito_Kiri`"""

  lordpengimg = "https://telegra.ph/file/689f2d3b1f5f2ae4d3005.png"
  lordpeng = """[Lord ZoldyckFamily」](https://telegram.dog/LordPeng) as Illumi Zoldyck.\n To get more about him do `!info @LordPeng`"""
  
  Chinmayimg = "https://telegra.ph/file/16cc60c94d7ff535e3957.png"
  Chinmay = """[Chinmay🇮🇳 ZoldyckFamily」](https://telegram.dog/Chinmay888) as Leorio Paradinight.\n To get more about him do `!info @Chinmay888`"""
  
  Muzammilimg = "https://telegra.ph/file/335efcdd8ffb462371582.png"
  Muzammil = """[Muzammil ZoldyckFamily」](https://telegram.dog/drakxtor) as my elder brother Killua Zoldyck.\n To get more about him do `!info @drakxtor`"""
  
  Masterimg = "https://telegra.ph/file/37bf67a10d77b9661bec1.png"
  Master = """[Master](https://telegram.dog/Master_yodhaa) as my father Silva Zoldyck.\n To get more about him do `!info @Master_yodhaa`"""

  anujimg = "https://telegra.ph/file/d4888fcbdeb3261a2a9cf.png"
  anuj = """[Anuj「ZoldyckFamily」](https://telegram.dog/zeroxknown) as Chrollo Lucilfer.\n To get more about him do `!info @zeroxknown`"""
  
  saharshimg = "https://telegra.ph/file/348ae7fcba0116a9a4314.jpg"
  saharsh = """[Saharsh DHMN! ZoldyckFamily」](https://telegram.dog/MedevilofMarvel) as Meruem.\n To get more about him do `!info @MedevilofMarvel`"""


 

  message.reply_photo(sunnyimg,sunny, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(bhavikimg, bhavik, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(drakxtorimg, drakxtor, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(alokimg, alok, parse_mode=ParseMode.MARKDOWN) 
  message.reply_photo(neelimg, neel, parse_mode=ParseMode.MARKDOWN)  
  message.reply_photo(kiritoimg, kirito, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(lordpengimg, lordpeng, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(Chinmayimg, Chinmay, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(Masterimg, Master, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(anujimg, anuj, parse_mode=ParseMode.MARKDOWN)
  message.reply_photo(saharshimg, saharsh, parse_mode=ParseMode.MARKDOWN)

__help__ = """
 - /familylist 
"""

__mod_name__ = "Zoldyck Family "
  
ud_handle = DisableAbleCommandHandler("familylist", ud)

dispatcher.add_handler(ud_handle)
