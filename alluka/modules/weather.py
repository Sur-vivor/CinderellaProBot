import pyowm
import json
import requests

from pyowm import timeutils, exceptions
from telegram import Message, Chat, Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import run_async

from alluka import dispatcher, updater, API_WEATHER, API_ACCUWEATHER
from alluka.modules.disable import DisableAbleCommandHandler

from alluka.modules.helper_funcs.alternate import send_message

@run_async
def weather(update, context):
    args = context.args
    location = " ".join(args)
    if location.lower() == context.bot.first_name.lower():
        send_message(update.effective_message, "I will keep watching when I am happy or sad!")
        context.bot.send_sticker(update.effective_chat.id, BAN_STICKER)
        return

    try:
        owm = pyowm.OWM(API_WEATHER)
        observation = owm.weather_at_place(location)
        theweather = observation.get_weather()
        obs = owm.weather_at_place(location)
        getloc = obs.get_location()
        thelocation = getloc.get_name()
        temperature = theweather.get_temperature(unit='celsius')['temp']
        fc = owm.three_hours_forecast(location)

        # Weather symbols
        status = ""
        status_now = theweather.get_weather_code()
        if status_now < 232: # Rain storm
            status += "⛈️ "
        elif status_now < 321: # Drizzle
            status += "🌧️ "
        elif status_now < 504: # Light rain
            status += "🌦️ "
        elif status_now < 531: # Cloudy rain
             status += "⛈️ "
        elif status_now < 622: # Snow
            status += "🌨️ "
        elif status_now < 781: # Atmosphere
            status += "🌪️ "
        elif status_now < 800: # Bright
            status += "🌤️ "
        elif status_now < 801: # A little cloudy
             status += "⛅️ "
        elif status_now < 804: # Cloudy
             status += "☁️ "
        status += theweather._detailed_status
                    

        weathertmr = tomorrow.get_weather_code()

        send_message(update.effective_message, "{} today is {}, around {}°C.\n").format(thelocation,
                status, temperature)

    except pyowm.exceptions.api_call_error.APICallError:
        send_message(update.effective_message, "Write the location to check the weather")
    except pyowm.exceptions.api_response_error.NotFoundError:
        send_message(update.effective_message, "Sorry, location not found 😞")
    else:
        return

@run_async
def accuweather(update, context):
    chat_id = update.effective_chat.id
    message = update.effective_message
    args = context.args
    if not args:
        return send_message(update.effective_message, "Enter the name of the location to check the weather!")
    location = " ".join(args)
    if location.lower() == context.bot.first_name.lower():
        send_message(update.effective_message, "I will keep watching when I am happy or sad!")
        context.bot.send_sticker(update.effective_chat.id, BAN_STICKER)
        return

    if True:
        url = "http://api.accuweather.com/locations/v1/cities/search.json?q={}&apikey={}".format(location, API_ACCUWEATHER)
        headers = {'Content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        try:
            data = r.json()[0]
        except:
            return send_message(update.effective_message, "Sorry, location not found 😞")
        locid = data.get('Key')
        urls = "http://api.accuweather.com/currentconditions/v1/{}.json?apikey={}&details=true&getphotos=true".format(locid, API_ACCUWEATHER)
        rs = requests.get(urls, headers=headers)
        datas = rs.json()[0]

        if datas.get('WeatherIcon') <= 44:
            icweather = "☁"
        elif datas.get('WeatherIcon') <= 42:
            icweather = "⛈"
        elif datas.get('WeatherIcon') <= 40:
            icweather = "🌧"
        elif datas.get('WeatherIcon') <= 38:
            icweather = "☁"
        elif datas.get('WeatherIcon') <= 36:
            icweather = "⛅"
        elif datas.get('WeatherIcon') <= 33:
            icweather = "🌑"
        elif datas.get('WeatherIcon') <= 32:
            icweather = "🌬"
        elif datas.get('WeatherIcon') <= 31:
            icweather = "⛄"
        elif datas.get('WeatherIcon') <= 30:
            icweather = "🌡"
        elif datas.get('WeatherIcon') <= 29:
            icweather = "☃"
        elif datas.get('WeatherIcon') <= 24:
            icweather = "❄"
        elif datas.get('WeatherIcon') <= 23:
            icweather = "🌥"
        elif datas.get('WeatherIcon') <= 19:
            icweather = "☁"
        elif datas.get('WeatherIcon') <= 18:
            icweather = "🌨"
        elif datas.get('WeatherIcon') <= 17:
            icweather = "🌦"
        elif datas.get('WeatherIcon') <= 15:
            icweather = "⛈"
        elif datas.get('WeatherIcon') <= 14:
            icweather = "🌦"
        elif datas.get('WeatherIcon') <= 12:
            icweather = "🌧"
        elif datas.get('WeatherIcon') <= 11:
            icweather = "🌫"
        elif datas.get('WeatherIcon') <= 8:
            icweather = "⛅️"
        elif datas.get('WeatherIcon') <= 5:
            icweather = "☀️"
        else:
            icweather = ""

        weather = "*{} {}*\n".format(icweather, datas.get('WeatherText'))
        weather += (update.effective_message, "*Temperature:* `{}°C`/`{}°F`\n").format(datas.get('temperature').get('Metric').get('Value'), datas.get('temperature').get('Imperial').get('Value'))
        weather += (update.effective_message, "*Humidity:* `{}`\n").format(datas.get('RelativeHumidity'))
        direct = "{}".format(datas.get('Wind').get('Direction').get('English'))
        direct = direct.replace("N", "↑").replace("E", "→").replace("S", "↓").replace("W", "←")
        weather += (update.effective_message, "*Wind:* `{} {} km/h` | `{} mi/h`\n").format(direct, datas.get('Wind').get('Speed').get('Metric').get('Value'), datas.get('Wind').get('Speed').get('Imperial').get('Value'))
        weather += (update.effective_message, "*UV level:* `{}`\n").format(datas.get('UVIndexText'))
        weather += (update.effective_message, "*Pressure:* `{}` (`{} mb`)\n").format(datas.get('PressureTendency').get('LocalizedText'), datas.get('Pressure').get('Metric').get('Value'))

        lok = []
        lok.append(data.get('LocalizedName'))
        lok.append(data.get('AdministrativeArea').get('LocalizedName'))
        for x in reversed(range(len(data.get('SupplementalAdminAreas')))):
            lok.append(data.get('SupplementalAdminAreas')[x].get('LocalizedName'))
        lok.append(data.get('Country').get('LocalizedName'))
        text = (update.effective_message, "*Current weather in {}*\n").format(data.get('LocalizedName'))
        text += "{}\n".format(weather)
        text += (update.effective_message, "*Location:* `{}`\n\n").format(", ".join(lok))

        # try:
        #     context.bot.send_photo(chat_id, photo=datas.get('Photos')[0].get('LandscapeLink'), caption=text, parse_mode="markdown", reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="More info", url=datas.get('Link'))]]))
        # except:
        send_message(update.effective_message, text, parse_mode="markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="More info", url=datas.get('Link'))]]))


__help__ = """
 - /weather <city>: get weather info in a particular place
"""

__mod_name__ = "Weather"

WEATHER_HANDLER = DisableAbleCommandHandler("weather", accuweather, pass_args=True)
#ACCUWEATHER_HANDLER = DisableAbleCommandHandler("accuweather", accuweather, pass_args=True)


dispatcher.add_handler(WEATHER_HANDLER)
#dispatcher.add_handler(ACCUWEATHER_HANDLER)