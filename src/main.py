#! /usr/bin/python
# -
# *- coding: utf-8 -*-
"""
WEB SCRAPING 
Date: '24 MAR 2024'
Update: '24 MAR 2024'
Author: Marco De Stavola '
"""

from package import scraper, AddMessage
import pandas as pd
import requests
import json
import os
import sys
from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page  

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

## READ CONFIG FILE FOR DEV
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

# GET A JSON FROM REQUEST OF IMMOBILLIARE WEBSITE    
# url_zones_immobiliare = f"{url}{update.message.text}"
url_zones_immobiliare = f"{url}{city}"
response = requests.get(url_zones_immobiliare)
print(url_zones_immobiliare)
print(response)
# zones_immobiliare = json.loads(response.text)

