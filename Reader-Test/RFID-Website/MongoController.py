from pymongo import MongoClient

class DBClient:
	def __init__(self):
		self.client = MongoClient()			
		self.db = self.client.DBPasswords				#Database
		self.passwords = self.db.passwords				#Collection
	def pws(self):
		return self.passwords
	