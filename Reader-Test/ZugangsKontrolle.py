import mfrc522
import time
import RPi.GPIO as GPIO
import hashlib

class Zugang:
	def __init__(self):
		self.mfReader = mfrc522.MFRC522()
		self.reading  = False
		self.block = 4
		self.key = [0x53,0x49,0x43,0x48,0x45,0x52]
		self.password = "019060a49294980fa41039fb380090a4fe869c4f25d14907a0f9acaa0dc45d00"	#Password has been hashed with sha256

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

z = Zugang()
print(z.authorizedWrapper())