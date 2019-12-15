import pymysql


class DataBase:

	def __init__(self, host, user, passwd, db="mysql", charset='utf8'):

		self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)							   
		self.cur = self.conn.cursor()

		print(self.conn.open)

	def use_table(self, tableName):

		self.cur.execute("USE "+tableName)


	def execution(self, sql):
			
		self.cur.execute(sql)

		try:
			self.conn.commit()       
		except:
			self.conn.rollback()

			self.conn.close()

	def executemany(self, sql, args):

		self.cur.executemany(sql, args)

		try:
			self.conn.commit()       
		except:
			self.conn.rollback()

			self.conn.close()


	def fetch(self, fetch):

		if fetch == 'one':
			return self.getAlone(self.cur.fetchone())
		else:
			return self.cur.fetchall()

	def getAlone(self, fetchdata):

		if len(fetchdata) == 1:
			fetchdata = fetchdata[0]

		return fetchdata