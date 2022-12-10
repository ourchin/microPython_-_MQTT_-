import serial
import time


ser = srial.Serial("/dev/tty.usbserial-14120",115200)

while True:
	conect = "aa"
	data = bytes().fromhex(content)
	ser.write(data)
	time.sleep(1)
	print(data)