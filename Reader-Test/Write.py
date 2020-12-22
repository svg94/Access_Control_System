import RPi.GPIO as GPIO
import mfrc522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = mfrc522.MFRC522()

def write():
	global continue_reading
	while continue_reading:
    
		# Scan for cards
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		# If a card is found
		if status == MIFAREReader.MI_OK:
			print ("Card detected")
    
		# Get the UID of the card
		(status,uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:

			# Print UID
			print(uid)

			# This is the default key for authentication
			key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
			#key = [0x53, 0x49, 0x43, 0x48, 0x45, 0x52]
			# Select the scanned tag
			MIFAREReader.MFRC522_SelectTag(uid)

			# Authenticate
			status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 7, key, uid)

			# Check if authenticated
			if status == MIFAREReader.MI_OK:

				# Variable for the data to write
				#data = [0x53, 0x48, 0x45, 0x52, 0x4c, 0x4f, 0x43, 0x4b] #SHERLOCK
				data = [0x53, 0x49, 0x43, 0x48, 0x45, 0x52, 0xFF, 0x07, 0x80, 0x69, 0x53, 0x49, 0x43, 0x48, 0x45, 0x52]
				# Fill the data with 0xFF
				#for x in range(0,8):
				#	data.append(0x00)

			
				MIFAREReader.MFRC522_Write(7, data)
				print ("It now looks like this:")
				print (MIFAREReader.MFRC522_Read(7))

				MIFAREReader.MFRC522_StopCrypto1()
				# Make sure to stop reading for cards
				continue_reading = False
			else:
				print ("Authentication error")
write()