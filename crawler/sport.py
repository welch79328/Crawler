import os
import sys
import json
import time
import re
import datetime
import platform
from config import config
from selenium.common.exceptions import TimeoutException
from .base import Base


class Sport(Base):

	def __init__(self):

		self.start = time.time()
		self.sportData = config.selenium.getSportData(config.SPORT_ACTIVE_CATEGORIES_URL)
		self.liveSportData = config.selenium.getSportData(config.SPORT_LIVE_GAMES_URL)
		self.tournamentId = {'s-441':'441', 's-451':'399', 's-442':'501', 's-443':'502', 's-445':'503', 's-446':'521', \
							 's-447':'461', 's-647':'661', 's-650':'561', 's-664':'541', 's-651':'601', 's-663':'542', \
							 's-455':'11111111', 's-456':'11111111', 's-646':'462',  's-652':'621', 's-450':'11111111', \
							 's-661':'581', 's-662':'11111111'}
		self.categoriesArr = ['s-441','s-442','s-443','s-444','s-445','s-446','s-447','s-450','s-451','s-455','s-456', \
							  's-646','s-647','s-650','s-651','s-652','s-661','s-663','s-664','s-662']


	def championGamesLogic(self, gemeType, jsonFileName=''):

		jsonFilePath = config.JSON_PATH+jsonFileName+'.json'

		if not (os.path.isfile(jsonFilePath ) )or int(time.strftime("%M", time.localtime()))%15 == 0:
			self.championGamesGetUrl(jsonFilePath)
		elif os.path.isfile(jsonFilePath ):
			jsonFile = open(jsonFilePath ,"r")
			fileContent = jsonFile.read()
			if not fileContent == '':
				jsonlist = json.loads(fileContent)

				sql = "DELETE FROM `champion_games`"
				config.dataBase.execution(sql)

				for key, value in jsonlist.items():
					tournament = key
					for dictList in value:
						for subCategorieId in dictList:

							url = dictList[subCategorieId]
							gameJsonData = config.selenium.getSportData(url)

							print(url.encode('utf-8'))
							print(gameJsonData.encode('utf-8'))
							print('---------')
							if not gameJsonData == '[]':
								sql = "insert into champion_games(`tid`,`groups`,`gamejson`,`updatetime`) values ('%s','%s','%s','%s')" % \
									(subCategorieId, tournament, gameJsonData, self._getCurTime())
								config.dataBase.execution(sql)

	def gameResultLogic(self, gemeType):

		categoriesJsonData = json.loads(self.sportData)

		sql = "DELETE FROM " + gemeType
		config.dataBase.execution(sql)

		if not categoriesJsonData == []:
			for category in self.categoriesArr:

				if category =='s-441':
					pages = 4
				else:
					pages = 2

				for page in range(1,pages+1):
					
					sportId = category
					url = "https://www.sportslottery.com.tw/web/services/rs/betting/results/15102/3.json?sportId=" \
							+ sportId + "&page=" + str(page) + "&locale=tw&brandId=defaultBrand&channelId=1"
					JsonData = config.selenium.getSportData(url)
					print(JsonData.encode('utf-8'))

					if (JsonData !='false' 
						and JsonData !='{"betGameResults":[],"lexicon":{"resources":{},"locale":"tw"},"p":1}'
		            	and JsonData !='{"betGameResults":[],"lexicon":{"resources":{},"locale":"tw"},"p":0}'
		                and JsonData !='{"betGameResults":[],"lexicon":{"resources":{},"locale":"tw"},"p":2}'):
						
						sql = "insert into gameresult(`cateid`,`page`,`gamejson`,`updatetime`) values ('%s','%s','%s','%s')" % \
							(sportId, page, JsonData, self._getCurTime())
						config.dataBase.execution(sql)

	def gamesLogic(self, gemeType):

		categoriesJsonData = json.loads(self.sportData)

		sql = "DELETE FROM " + gemeType
		config.dataBase.execution(sql)

		for category in categoriesJsonData:
					
			categoryId = category["categoryId"]
			numOfGames = str(category["numOfGames"])

			url = 'https://www.sportslottery.com.tw/web/services/rs/betting/games/15102/0.json?status=active&limit=' \
					+ numOfGames + '&action=excludeTournamentWithExceptionPriority&marketLimit=1&sportId=' \
					+ categoryId + '&locale=tw&brandId=defaultBrand&channelId=1'
			categoryJsonData = config.selenium.getSportData(url)
			print(categoryJsonData.encode('utf-8'))

			if not categoryJsonData == '[]':
				sql = "insert into games(`cateid`,`gamejson`,`updatetime`) values ('%s','%s','%s')" % \
					(categoryId, categoryJsonData, self._getCurTime())
				config.dataBase.execution(sql)

	def liveGamesLogic(self, gemeType):

		liveGamesJsonData = json.loads(self.liveSportData)

		sql = "DELETE FROM " + gemeType
		config.dataBase.execution(sql)

		for game in liveGamesJsonData:

			ni = str(game['ni'])
			url = 'https://www.sportslottery.com.tw/web/services/rs/betting/liveGames/15102/0.json?nevIds=' \
					+ ni + '&locale=tw&brandId=defaultBrand&channelId=1'

			gameJsonData = config.selenium.getSportData(url)
			print(gameJsonData.encode('utf-8'))

			if not gameJsonData == '[]':
				
				sql = "insert into livegames(`ni`,`gamejson`,`updatetime`) values ('%s','%s','%s')" % \
		   			(ni, gameJsonData, self._getCurTime())
				config.dataBase.execution(sql)

	def singleGamesLogic(self, gemeType):

		sqlArray = []
		categoriesJsonData = json.loads(self.sportData)

		sql = "DELETE FROM `singlegames` WHERE updatetime < '%s'" % \
			(self._firstTenMinutes())
		config.dataBase.execution(sql)

		if categoriesJsonData == []:
			sql = "DELETE FROM " + gemeType
			config.dataBase.execution(sql)
			sys.exit()

		sql = "SELECT * FROM sport_position"
		config.dataBase.execution(sql)
		preCategory = config.dataBase.fetch('one')[1]

		curCategory = preCategory + 1
		if curCategory >= len(categoriesJsonData):	
			curCategory = 0

		sql = "UPDATE sport_position SET position = '%s'" % \
			(curCategory)

		config.dataBase.execution(sql)

		categoryId = categoriesJsonData[curCategory]["categoryId"]
		numOfGames = str(categoriesJsonData[curCategory]["numOfGames"])
		url = 'https://www.sportslottery.com.tw/web/services/rs/betting/games/15102/0.json?status=active&limit=' \
				+ numOfGames + '&action=excludeTournamentWithExceptionPriority&marketLimit=1&sportId=' \
				+ categoryId + '&locale=tw&brandId=defaultBrand&channelId=1'

		categoryJsonData = json.loads(config.selenium.getSportData(url))

		for game in categoryJsonData:

			lv = 0
			ni = str(game["ni"])
			lv = int(game["lv"] == 'true')
			kdt = str(game["kdt"])[0:10]
			url = 'https://www.sportslottery.com.tw/web/services/rs/betting/games/15102/0.json?eventMethods=1&' \
					'eventMethods=2&nevIds='+ni+'&locale=tw&brandId=defaultBrand&channelId=1'

			gameJsonData = config.selenium.getSportData(url)
			
			print(gameJsonData.encode('utf-8'))
			print('----------')
			if not gameJsonData == '[]':
				sqlArray.append((curCategory, ni, lv, kdt, gameJsonData, self._getCurTime()))

		sql = "DELETE FROM `singlegames` WHERE position = '%s'" % \
			(curCategory)
		config.dataBase.execution(sql)

		if not sqlArray == []:	
			sql = "insert into singlegames(`position`,`ni`,`lv`,`kdt`,`gamejson`,`updatetime`) values (%s,%s,%s,%s,%s,%s)"
			config.dataBase.executemany(sql, sqlArray)

	def championGamesGetUrl(self, jsonFilePath=''):

		jsonlist = {}
		categoriesData = self.sportData
		categoriesJsonData = json.loads(categoriesData)

		sql = "DELETE FROM `sport_type`"
		config.dataBase.execution(sql)

		if not categoriesJsonData == []: 
			sql = "insert into sport_type(`gamejson`,`updatetime`) values ('%s','%s')" % \
				(categoriesData, self._getCurTime())
			config.dataBase.execution(sql)

			for category in categoriesJsonData:
				subCategories = category['subCategories']
				categoryId = category['categoryId']
				if categoryId in self.tournamentId:
					tournament = self.tournamentId[categoryId]
				else:
					tournament = '641'
				jsonlist[tournament] = []

				for subCategory in subCategories:
					subSubCategories = subCategory['subCategories']
					for subSubCategory in subSubCategories:

						subSubCategoryId = subSubCategory['categoryId']
						url = 'https://www.sportslottery.com.tw/web/services/rs/betting/tournamentGames/15102/0/'+ subSubCategoryId + \
								'.json?groups=' + tournament + '&locale=tw&brandId=defaultBrand&channelId=1'
						if subSubCategoryId == 't-4092':
							url = 'https://www.sportslottery.com.tw/web/services/rs/betting/tournamentGames/15102/0/t-4092.json?' \
									'groups=502&groups=641&locale=tw&brandId=defaultBrand&channelId=1'
						elif subSubCategoryId == 't-4104':
							url = 'https://www.sportslottery.com.tw/web/services/rs/betting/tournamentGames/15102/0/t-4104.json?' \
									'groups=861&groups=11111111&locale=tw&brandId=defaultBrand&channelId=1'

						try:
							gameJsonData = config.selenium.getSportData(url)

							print(url.encode('utf-8'))
							print(gameJsonData.encode('utf-8'))
							print('---------')
							if not gameJsonData == '':
								jsonlist[tournament].append({subSubCategoryId:url})
						except:
							print('Not Find Url')																
							config.driver.quit()

			with open(jsonFilePath,"w") as f:
				json.dump(jsonlist,f)
				print("加载入文件完成...".encode('utf-8'))

	def announcementLogic(self, gemeType):

		urls = []
		today = datetime.date.today()
		yesterday = today - datetime.timedelta(days=1)
		todayGeneralCalendar = self._getGeneralCalendar(today)
		yesterdayGeneralCalendar = self._getGeneralCalendar(yesterday)

		config.selenium.getSportData(config.SPORT_ANNOUNCEMENT_URL)
		datas = config.driver.find_elements_by_class_name("results-row")

		for data in datas:
			judgeText = ''
			a = data.find_element_by_tag_name("a")
			text = a.text
			href = a.get_attribute("href")
			machiningText = re.split(u"[\u4e00-\u9fa5]+", text)
			for filterText in machiningText:
				judgeText+=filterText
			if todayGeneralCalendar == judgeText or yesterdayGeneralCalendar == judgeText:
				urls.append(href)
		sql = "DELETE FROM `sport_announcement`"
		config.dataBase.execution(sql)
		urls.reverse()
		for url in urls:
			p_content = ''	
			config.selenium.getSportData(url)
			datas = config.driver.find_element_by_class_name("journal-content-article")
			h2 = datas.find_element_by_tag_name("h2").get_attribute('innerHTML')
			p = datas.find_elements_by_tag_name("p")
			h2 = h2.split('<em>', 1 )
			h2 = h2[0].strip()
			print(h2.encode('utf-8'))
			for x in p:
				if x.text != '':
					p_content += '<p>'+x.get_attribute('innerHTML').strip()+'</p>'
			print(p_content.encode('utf-8'))
			sql = "insert into sport_announcement(`title`,`content`,`updatetime`) values ('%s','%s','%s')" % \
				(h2, p_content, self._getCurTime())

