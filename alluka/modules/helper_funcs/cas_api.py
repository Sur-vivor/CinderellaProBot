import urllib.request as url
import json
import datetime

DEVUSER = "" #user ID that is banned for testing
VERSION = "1.3.2 - DEV"
CAS_QUERY_URL = "https://api.cas.chat/check?user_id="
DL_DIR = "./csvExports"

def get_user_data(user_id):
    with url.urlopen(CAS_QUERY_URL + str(user_id)) as userdata_raw:
        userdata = json.loads(userdata_raw.read().decode())
        return userdata

def isbanned(userdata):
    return userdata['ok']

def banchecker(user_id):
    if(str(user_id) == DEVUSER):
        return True
    return isbanned(get_user_data(user_id))

def vercheck() -> str:
    return str(VERSION)

def offenses(user_id):
    if str(user_id) == DEVUSER:
        return "TEST USER"
    userdata = get_user_data(user_id)
    try:
        offenses = userdata['result']['offenses']
        return str(offenses) 
    except:
        return None
    
def timeadded(user_id):
    if str(user_id) == DEVUSER:
        return "TEST USER - NEVER"
    userdata = get_user_data(user_id)
    try:
        timeEp = userdata['result']['time_added']
        timeHuman = datetime.datetime.utcfromtimestamp(timeEp).strftime('%H:%M:%S, %d-%m-%Y')
        return timeHuman
    except:
        return None
