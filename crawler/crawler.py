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

		Sport().getSingleGames()

	def run(self, gemeType='', maxExecutionTime=0, sleepTime=0):

		start = self._getTime()
		while self.executionTime <= int(maxExecutionTime):
			try:
				self._selectionParameter(gemeType)
			except TimeoutException:
				config.driver.delete_all_cookies()
				print('timeout')

			time.sleep(int(sleepTime))
			end = self._getTime()
			self.executionTime = end - start
			print(self.executionTime)

		config.driver.quit()