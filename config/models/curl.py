from urllib.parse import urlencode
import pycurl
import json


class Curl():

	def __init__(self):
		self.pycurl_connect = pycurl.Curl()
		self.pycurl_connect.setopt(pycurl.POST, 1)
		self.pycurl_connect.setopt(pycurl.SSL_VERIFYPEER, False)
		self.pycurl_connect.setopt(pycurl.SSL_VERIFYHOST, False)

	def post(self, url, data):

		if isinstance (data, str):
			header = ['Content-Type: application/x-www-form-urlencoded']
			data = urlencode({'messages': data + ' 偵測異常'})
		elif isinstance (data, dict):
			header = ['Content-Type: application/json']
			data = json.dumps(data)

		self.pycurl_connect.setopt(pycurl.URL, url)
		self.pycurl_connect.setopt(pycurl.HTTPHEADER, header)
		self.pycurl_connect.setopt(pycurl.POSTFIELDS, data)
		self.pycurl_connect.perform()