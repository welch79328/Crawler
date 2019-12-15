import json
import time
from config import config
from .base import Base


class Sport(Base):

	def __init__(self):
		super().__init__()
		self.chart = self.getPlayCode()['lexicon']['resources']
		self.sportData = config.selenium.getSportData(config.SPORT_ACTIVE_CATEGORIES_URL)


	def getSingleGames(self):

		normalGamesjson = {}
		self.contrastJson = {
			's':{},
			'c':{},
			't':{},
			'n':{}
		}
		categoriesData = self.sportData
		# 取得運動及賽事列表
		categoriesJsonData = json.loads(categoriesData)

		for categoryLevelOne in categoriesJsonData:
			
			categoryLevelOneId = categoryLevelOne["categoryId"]
			categoryLevelOnenumOfGames = str(categoryLevelOne["numOfGames"])
			normalGamesjson[categoryLevelOneId] = {}
			self.contrastJson['s'][categoryLevelOneId] = categoryLevelOne["name"].rstrip()

			for categoryLevelTwo in categoryLevelOne['subCategories']:
				normalGamesjson[categoryLevelOneId][categoryLevelTwo['categoryId']] = {}
				self.contrastJson['c'][categoryLevelTwo['categoryId']] = categoryLevelTwo["name"]
				for categoryLevelThree in categoryLevelTwo['subCategories']:
					normalGamesjson[categoryLevelOneId][categoryLevelTwo['categoryId']][categoryLevelThree['categoryId']] = {}
					self.contrastJson['t'][categoryLevelThree['categoryId']] = categoryLevelThree["name"]

			url = 'https://www.sportslottery.com.tw/web/services/rs/betting/games/15102/0.json?status=active&limit=' \
					+ categoryLevelOnenumOfGames + '&action=excludeTournamentWithExceptionPriority&marketLimit=1&sportId=' \
					+ categoryLevelOneId + '&locale=tw&brandId=defaultBrand&channelId=1'

			categoryJsonData = json.loads(config.selenium.getSportData(url))

			for game in categoryJsonData:

				ni = str(game["ni"])
				url = 'https://www.sportslottery.com.tw/web/services/rs/betting/games/15102/0.json?eventMethods=1&' \
						'eventMethods=2&nevIds='+ni+'&locale=tw&brandId=defaultBrand&channelId=1'

				try:
					gameJsonData = json.loads(config.selenium.getSportData(url))
					normalGamesjson[game['si']][game['ci']][game['ti']]['n-'+str(game['ni'])] = self.processGame(game, gameJsonData[0])
				except:
					pass
				time.sleep(5)
			
		normalGamesjsonFilePath = config.JSON_PATH+'/normalGames.json'
		contrastJsonFilePath = config.JSON_PATH+'/contrast.json'

		with open(normalGamesjsonFilePath,"w") as f, open(contrastJsonFilePath,"w") as fc:
			json.dump(normalGamesjson, f)
			json.dump(self.contrastJson, fc)
			print("加载入文件完成...")


	def processGame(self, game, betJson):

		ti = game['ti'] #比賽聯盟編號
		si = game['si'] #運動編號
		ni = game['ni'] # 一般賽事編號
		ai = game['ai'] # 隊伍編號
		hi = game['hi'] # 隊伍編號
		gameCode = game['code'] # 賽事編號
		awayTeam = game['lexicon']['resources'][ai] # 客隊名稱
		homeTeam = game['lexicon']['resources'][hi] # 主隊名稱
		gameTime = self.strtotime(game['kdt'], 10) #開賽時間(只取10位數)

		# print(game)
		# print('主隊名稱:' + homeTeam)
		# print('客隊名稱:' + awayTeam)
		print('標題:' + homeTeam + ' VS ' + awayTeam)
		self.contrastJson['n']['n-'+str(ni)] = homeTeam + ' VS ' + awayTeam
		# print('開賽時間:' + gameTime)
		trt = self.isset(betJson, ['trt'])
		prt = self.isset(betJson, ['prt'])
		vsp = self.isset(betJson, ['vsp'], False)
		hpp = self.isset(betJson, ['hpp'], False)
		status = betJson['status']

		# 籃球
		NumberOfBoard = self.NumberOfBoard(vsp, hpp) # 比賽節數
		# 棒球
		if (si == 's-443' and self.isset(betJson, ['competitors']) != ''):
			competitors = betJson['competitors']
			awaySP = betJson['lexicon']['resources'][competitors['a']] # 客隊先發投手
			homeSP = betJson['lexicon']['resources'][competitors['h']] # 主隊先發投手
		else:
			awaySP = ''
			homeSP = ''

		playCode = []
		# 玩法
		for play in betJson['markets']:

			titleCode = 'def_' + si + '_' + play['i'] # 取得比賽的玩法名稱

			if titleCode == 'def_s-443_3':
				title = self.zhPeriod(si, numberOfBoard)
			else:
				title = self.chart[titleCode]

			codes = []
			# 玩法賠率
			for betInfo in play['codes']:

				optionCode = betInfo['c']
				odds = self.isset(betInfo, ['oddPerSet','1'], 1.0) # 得到賠率
				option = self.chart[titleCode + '_' + str(optionCode)]
				Options = self.dealStringToZhtw(option, awayTeam, homeTeam, awaySP, homeSP) # 取代名稱
				codes.append({
					'name':Options, # 玩法名稱
					'odds':odds, # 賠率
				})
			# 該運動單一玩法有的賠率
			playCode.append({
				'title':title, 
				'codes':codes
			})

		return {
			'homeTeam':homeTeam,
			'awayTeam':awayTeam,
			'gameTime':gameTime,
			'gameCode':gameCode,
			'playCode':playCode
		}








