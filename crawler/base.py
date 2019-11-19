import os
import sys
import time
import random
import requests
import subprocess
import datetime
from config import config


class Base():

	def __init__(self):
		pass

	def _getTime(self):
		return time.time()

	def _getCurTime(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

	def _firstTenMinutes(self):
		return (datetime.datetime.now()-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")

	def _getGeneralCalendar(self, day):

		day = int(day.strftime("%Y%m%d"))
		generalCalendar = str(day - 19110000)

		return generalCalendar

	def _pingIP(self):

		try:
			response = requests.get(config.SPORT_BASE_URL, timeout=10)
		except:
			return True

			return False

	def _ec2Process(self):
		currentInstanceID = str(subprocess.check_output("wget -q -O - http://169.254.169.254/latest/meta-data/instance-id", shell=True), encoding = "utf-8")

		sql = "SELECT zone, category, country FROM ec2_list WHERE Instance_ID = '%s'" % \
			(currentInstanceID)
		config.dataBase.execution(sql)
		result = config.dataBase.fetch('one')

		currentRegion = result[0]
		webCrawlerName = result[1]
		currentcountry = result[2]

		currentData = {'region':currentRegion, 'instanceID':currentInstanceID}

		responseResult = currentcountry + ':' + webCrawlerName
		config.curl.post(config.CURL_LINEMESSAGE_URL, responseResult)

		sql = "SELECT Instance_ID, zone FROM ec2_list WHERE category = '%s' AND Instance_ID != '%s'" % \
			(webCrawlerName, currentInstanceID)
		config.dataBase.execution(sql)
		result = config.dataBase.fetch('all')
		
		backupMechanism = result[random.randint(0,len(result)-1)]

		instanceID = backupMechanism[0]
		region = backupMechanism[1]
		data = {'region':region, 'instanceID':instanceID}

		config.curl.post(config.CURL_EC2START_URL, data)
		config.curl.post(config.CURL_EC2STOP_URL, currentData)

