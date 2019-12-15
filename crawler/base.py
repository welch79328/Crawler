import time
import json
import requests
from config import config


class Base():

	def __init__(self):
		pass

	def _getTime(self):
		return time.time()

		# 時間戳轉時間
	def strtotime(self, timeData, length=False):

		if length:
			timeData = int(str(timeData)[0:length])

		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeData))

	def getPlayCode(self):

		f = open(config.DIRECTORY_PATH +'/crawler/json/play_code.json', 'r')
		playCode = json.loads(f.read())
		f.close()

		return playCode

	# 判斷是否有變數
	def isset(self, dict, keys, errResult=''):

		for key in keys:
			if type(key) == int:
				dict = dict[key]
			else:		
				if key in dict.keys():
					dict = dict[key]
				else:
					dict = errResult
					break
		return dict

	# 取得現在節數
	def NumberOfBoard(self, awayPeriod, homePeriod):

		index = 1
		if awayPeriod:
			for x in awayPeriod:
				pass

		return 1

	# 訂單顯示投注選項
	def zhPeriod(type, period):
		if type == 's-441':
			if period == '1':
				return '上半場'
			else:
				return '下半場'

		if type == 's-442':
			return '不讓分[第 ' + period + ' 節]'

		if type == 's-443':
			return '不讓分[第 ' + period + ' 局]'

		if type == 's-445':
			return '不讓分[第 ' + period + ' 盤]'

		if type == 's-650':
			return '不讓分[第 ' + period + ' 局]'

	def dealStringToZhtw(self, Option, awayteam, hometeam, awaySP='', homeSP=''):

		if self.isset(homeSP, []):
			homeSP = ' (' + homeSP + ')'

		if self.isset(awaySP, []):
			awaySP = ' (' + awaySP + ')'

		if Option.find('*1*/*2*') >= 0:
			Option = Option.replace('*1*/*2*', hometeam + homeSP + '/' + awayteam + awaySP)
		elif Option.find('*2*/*1*') >= 0:
			Option = Option.replace('*2*/*1*', awayteam + awaySP + '/' + hometeam + homeSP)
		elif Option.find('*1*') >= 0:
			Option = Option.replace('*1*', hometeam + homeSP)
		elif Option.find('*2*') >= 0:
			Option = Option.replace('*2*', awayteam + awaySP)
		return Option


	def outComeConditions(selection, OutcomeConditions):

		if selection.find('_') > 0:
			dealSelection = selection.split('_')
			selectionCode = dealSelection[1]
		else:
			selectionCode = selection

		if selectionCode == '446' or selectionCode == '448' or selectionCode == '449' or selectionCode == '450':
			if OutcomeConditions > 0:
				return '(-' + OutcomeConditions + ' +' + OutcomeConditions + ')'
			else:
				return '(+' + abs(OutcomeConditions) + ' -' + abs(OutcomeConditions) + ')'

		if selectionCode == '447' and OutcomeConditions > 0:
			return ' (' + (0 - OutcomeConditions) + ')'
		elif selectionCode == '445' and OutcomeConditions > 0:
			return ' (+' + abs(OutcomeConditions) + ')'
		elif selectionCode == '447' and OutcomeConditions < 0:
			return ' (+' + abs(OutcomeConditions) + ')'
		elif selectionCode == '452' and OutcomeConditions > 0:
			return ' (' + (0 - OutcomeConditions) + ')'
		elif selectionCode == '451' and OutcomeConditions > 0:
			return ' (+' + abs(OutcomeConditions) + ')'
		elif selectionCode == '452' and OutcomeConditions < 0:
			return ' (+' + abs(OutcomeConditions) + ')'
		elif selectionCode == '456' and OutcomeConditions > 0:
			return ' (' + (0 - OutcomeConditions) + ')'
		elif selectionCode == '455' and OutcomeConditions > 0:
			return ' (+' + abs(OutcomeConditions) + ')'
		elif selectionCode == '456' and OutcomeConditions < 0:
 			return ' (+' + abs(OutcomeConditions) + ')'
		else:
			return ' (' + OutcomeConditions + ')'

