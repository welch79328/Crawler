import sys
import os
import time
import requests
import subprocess
import random
import platform
from .models import (
	Selenium, DataBase, Curl
)

#------------Common Parameters---------------------------------------------
DIRECTORY_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

CHROME_DRIVER_PATH = DIRECTORY_PATH + "/drivers/"+platform.system()+"/chromedriver"
JSON_PATH = DIRECTORY_PATH + "/crawler/json/"

SPORT_BASE_URL = "https://www.sportslottery.com.tw"
SPORT_ACTIVE_CATEGORIES_URL = SPORT_BASE_URL+"/web/services/rs/betting/activeCategories/15102/0.json?locale=tw&brandId=defaultBrand&channelId=1"
SPORT_LIVE_GAMES_URL = SPORT_BASE_URL+"/web/services/rs/betting/liveGames/15102/0.json?locale=tw&brandId=defaultBrand&channelId=1"
SPORT_ANNOUNCEMENT_URL = SPORT_BASE_URL+'/zh/web/guest/betting-announcement'

#-------------------Curl-------------------------------------------------------

# CURL_LINEMESSAGE_URL = ''
# CURL_EC2START_URL = ''
# CURL_EC2STOP_URL = ''

# curl = Curl()

#-----------Import Class---------------------------------------------------
DEFAULT_DRIVER = CHROME_DRIVER_PATH
selenium = Selenium(DEFAULT_DRIVER)
driver = selenium.openrBowser()

#-----------MySql----------------------------------------------------------
# DB_HOST = ''
# DB_DATABASE = ''
# DB_USERNAME = ''
# DB_PASSWORD = ''

# dataBase = DataBase(DB_HOST, DB_USERNAME, DB_PASSWORD)
# dataBase.use_table(DB_DATABASE)
