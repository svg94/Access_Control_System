import mfrc522
import time
import RPi.GPIO as GPIO
import hashlib
from pymongo import MongoClient


class Zugang:
	def __init__(self):
		self.mfReader = mfrc522.MFRC522()
		self.client = MongoClient()			
		self.db = self.client.DBPasswords				#Database
		self.cardData = self.db.cardData				#Collection for Card Data Passwords, keys etc.
		self.reading  = False
		self.block = 12
		self.keyblock = 15
		keyData = self.cardData.find_one({"name": "data"}).get("key")	#Collection stores values as float, coverting in next line.
		self.key = [int(i) for i in keyData]			#0x53,0x49,0x43,0x48,0x45,0x52
		self.password = self.cardData.find_one({"name": "data"}).get("passwordHash")	#Password has been hashed with sha256

	def hashSha256(self, inp: str):	#securing password, so it's not written in plain text
		m = hashlib.sha256()
		m.update(inp.encode('utf-8'))
		return m.hexdigest() 
	
	def convert(self, inp: list):	#Converts List to String. Needed for hashing
		converted = "".join(str(e) for e in inp)
		return converted


	def authorized(self):
		self.mfReader
		self.reading = True
		while self.reading:
			time.sleep(1)											#Um Brute-Force and co zu verlangsamen und nicht moeglich zu machen.
			(status, tagtype) = self.mfReader.MFRC522_Request(self.mfReader.PICC_REQIDL)
			if status == self.mfReader.MI_OK:						#Karte finden
				(status, uid) = self.mfReader.MFRC522_Anticoll()	#AntiCollision getting id
				if status == self.mfReader.MI_OK:
					self.mfReader.MFRC522_SelectTag(uid)
					auth = self.mfReader.MFRC522_Auth(self.mfReader.PICC_AUTHENT1A, self.block, self.key, uid)
					if auth == self.mfReader.MI_OK:
						read = self.mfReader.MFRC522_Read(self.block)	#Reads data from Mifare Classic
						self.mfReader.MFRC522_StopCrypto1()
						if self.hashSha256(self.convert(read)) == self.password:	
							return True
						else:
							self.reading = False
					else:
						self.reading = False
			
		return False
	
	def authorizedWrapper(self):
		returnStatement = self.authorized()
		GPIO.cleanup()
		self.reading = False
		return returnStatement
	
	def checkCorrectDataInput(data):
		if len(data) == 16:
			return true
		return false

	def changeData(self,data,block):	#Changes 
		#if len(data)
		while True:
			time.sleep(1)											#Um Brute-Force and co zu verlangsamen und nicht moeglich zu machen.
			(status, tagtype) = self.mfReader.MFRC522_Request(self.mfReader.PICC_REQIDL)
			if status == self.mfReader.MI_OK:						#Karte finden
				(status, uid) = self.mfReader.MFRC522_Anticoll()	#AntiCollision getting id
				if status == self.mfReader.MI_OK:
					self.mfReader.MFRC522_SelectTag(uid)
					auth = self.mfReader.MFRC522_Auth(self.mfReader.PICC_AUTHENT1A, block, self.key, uid)
					if auth == self.mfReader.MI_OK:
						self.mfReader.MFRC522_Write(block, data)
						self.mfReader.MFRC522_StopCrypto1()
						return "successfully changed"
					else:
						return "Authentication Error"

	def changePassword(self, data):
		returnStatement = self.changeData(data,self.block)	
		password = self.hashSha256(self.convert(data))			#update MongoDB
		update = self.cardData.update_one({'name': "data"}, {"$set": {"name":"data","key": self.key,"passwordHash": password}})
		self.password = self.cardData.find_one({"name": "data"}).get("passwordHash")
		print(self.password)
		return returnStatement 			

	def changeKey(self, data):
		returnStatement = self.changeData(data, self.keyblock)
		key = data[:6]											#update MongoDB
		update  = self.cardData.update_one({'name': "data"}, {"$set": {"name":"data","key": key,"passwordHash": self.password}})
		fetchKey = self.cardData.find_one({"name": "data"}).get("key")
		self.key = [int(i) for i in fetchKey]
		return returnStatement

#z = Zugang()
#data = [0x53, 0x48, 0x45, 0x52, 0x4c, 0x4f, 0x43, 0x4b,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] #pw
#data = [0x53, 0x49, 0x43, 0x48, 0x45, 0x52, 0xFF, 0x07, 0x80, 0x69, 0x53, 0x49, 0x43, 0x48, 0x45, 0x52] #key
#print(z.changeKey(data))
#print(z.authorizedWrapper())
