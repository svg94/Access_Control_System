import hashlib
import string

def convertListToString(inp: list):
	converted = "".join(str(e) for e in inp)
	return converted

def hashSha256(inp: str):
	m = hashlib.sha256()
	m.update(inp.encode('utf-8'))
	return m.hexdigest()	#returns hexstring

stuff = convertListToString([0x53, 0x48, 0x45, 0x52, 0x4c, 0x4f, 0x43, 0x4b, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
x=hashSha256(stuff)
print(type(x))
print(x)