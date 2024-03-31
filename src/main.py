#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '24 MAR 2024'
Update: '24 MAR 2024'
Author: Marco De Stavola '
"""

import pandas as pd
import requests
import json
import os
import sys
from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page 
# from telegram.bot import Bot
from telegram.ext import *
# import keys
    
from package import Scraper, HandleText, AddMessage

TYPE = 1
QUERY_CITY = 2
QUERY_NEIGHBOURHOOD = 3
MACROZONE = 4
MIN_PRICE = 5
MAX_PRICE = 6
MIN_SURFACE = 7
MAX_SURFACE = 8
END = 9

RESULTS = 100

folder_name             = os.path.dirname(os.path.abspath(__file__))
OUTPUT_TMP      = folder_name + "\\OUTPUT_TMP"
LOG_FOLDER      = folder_name + "\\LOG\\"

#### LOG FOLDER AND FILE CREATION
try:
    if not os.path.exists(OUTPUT_TMP):
        os.makedirs(OUTPUT_TMP)
except Exception as e:
    print("Error OUTPUT_TMP folder cannot be created. Exception: " + str(e))
    sys.exit(1)
try:
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
except Exception as e:
    print("Error LOG_FOLDER folder cannot be created. Exception: " + str(e))
    sys.exit(1)

# GET A JSON FROM REQUEST OF IMMOBILLIARE WEBSITE  
try:
    JSON_FOLDER     = folder_name + "\\JSON"
    config_path = '\\'.join([JSON_FOLDER, 'config.json'])
    with open(config_path) as config_file:
        config = json.load(config_file)
        config = config["config"]
except Exception as e:
    JSON_FOLDER     = folder_name + "/JSON"
    config_path = '/'.join([JSON_FOLDER, 'config.json'])
    with open(config_path) as config_file:
        config = json.load(config_file)
        config = config["config"]  
url = config["url"]
city = config["city"]

async def start_commmand(update, context):
    await update.message.reply_text('Miaoooooo')

def main():
    # TOKEN = config.token
    TOKEN = '6845005306:AAHASISYw1H_hry4h3GO_expZhr13lxXdOI'
    # persistence = PicklePersistence(filename='../conversationbot')
    # my_persistence = PicklePersistence(filepath='../conversationbot')
    # create the updater, that will automatically create also a dispatcher and a queue to 
    # make them dialoge
    # bot = telegram.Bot(TOKEN)
    # updater = Updater(TOKEN, use_context=True)
    # updater = Updater(TOKEN,  update_queue=True)
    # dispatcher = updater.dispatcher

    application = Application.builder().token(TOKEN).build()
    # Commands
    application.add_handler(CommandHandler('start', start_commmand))
    # application.add_handler(CommandHandler('start', HandleText('start').start()))

    # Run bot
    application.run_polling(1.0)

    # add handlers for start and help commands
    # dispatcher.add_handler(CommandHandler("start", HandleText().start()))

    # url_zones_immobiliare = f"{url}{update.message.text}"
    # response = requests.get(url_zones_immobiliare)
    # result = Scraper(response).handle_rest_response()
    # print(result)
    # HandleText().text()
    # zones_immobiliare = json.loads(response.text)

    # updater.start_polling()
    # updater.idle()
    
if __name__ == '__main__':
    main()

