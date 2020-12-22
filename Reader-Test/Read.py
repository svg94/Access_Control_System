import RPi.GPIO as GPIO
import mfrc522
import signal
import time

continue_reading = True
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
block = 7

def end_read(signal, frame):
	global continue_reading
	print("ending read")
	continue_reading = False
	GPIO.cleanup()

def read():
	signal.signal(signal.SIGINT, end_read)

	MIFAREReader = mfrc522.MFRC522()

	print("Welcome to reader")

	while continue_reading:
		time.sleep(1)
		(status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	
		if status == MIFAREReader.MI_OK:
			print("card found")
		(status, uid) = MIFAREReader.MFRC522_Anticoll()

		if status == MIFAREReader.MI_OK:
			print(uid)
			MIFAREReader.MFRC522_SelectTag(uid)
			
			auth = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, block, key, uid)
			
			if auth == MIFAREReader.MI_OK:
				read = MIFAREReader.MFRC522_Read(block)
				MIFAREReader.MFRC522_StopCrypto1()
				print(read)
			else:
				print("Auth Err")
			
		
	
read()