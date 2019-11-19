import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from config import config
from .base import Base
from .sport import Sport
from selenium.common.exceptions import TimeoutException


class Crawler(Base):

	def __init__(self):

		self.executionTime = 0

	def _selectionParameter(self, gemeType=''):

		if gemeType == 'championgames':
			Sport().championGamesLogic(gemeType, 'championGames')
		elif gemeType == 'gameresult':
			Sport().gameResultLogic(gemeType)
		elif gemeType == 'games':
			Sport().gamesLogic(gemeType)
		elif gemeType == 'livegames':
			Sport().liveGamesLogic(gemeType)
		elif gemeType == 'singlegames':
			Sport().singleGamesLogic(gemeType)
		elif gemeType == 'announcement':
			Sport().announcementLogic(gemeType)
		elif gemeType == 'blockadeip':
			self.blockadeIP() 
		else:
			sys.exit()

	def run(self, gemeType='', maxExecutionTime=0, sleepTime=0):

		start = self._getTime()
		while self.executionTime <= int(maxExecutionTime):
			try:
				self._selectionParameter(gemeType)
			except TimeoutException:
				config.driver.delete_all_cookies()
				if self._pingIP():
					self._ec2Process()
				print('timeout')

			time.sleep(int(sleepTime))
			end = self._getTime()
			self.executionTime = end - start
			print(self.executionTime)

		config.driver.quit()

	def blockadeIP(self):
		
		while True:
			res = requests.get(config.SPORT_ACTIVE_CATEGORIES_URL)
			soup = BeautifulSoup(res.text, 'lxml')

			print (json.loads(str(soup)))



