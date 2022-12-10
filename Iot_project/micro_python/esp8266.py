import pyb
from pyb import Pin
import time
from pyb import UART


class ESP8266():

	def led_on(self):
		pyb.LED(4).on()

	def sta_mode(self):
		uart6 = UART(6, 115200)  #发送指令给ESP8266
		uart4 = UART(4, 115200)  #发送指令给PC

		uart4.write('setting sta mode.........\r\n\r\n')

		uart6.write('AT\r\n')
		uart4.write('Sending......... AT\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('Reply.........' + (str(tmp))[-7:-5] + '\r\n' + '\r\n')
					break

		uart6.write('AT+RST\r\n')
		uart4.write('Sending......... AT+RST\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-10:-5] == 'ready':
					uart4.write('Reply.........' + (str(tmp))[-10:-5] + '\r\n' + '\r\n')
					break

		uart6.write('AT+CWMODE_CUR=1\r\n')
		uart4.write('Sending......... AT+CWMODE_CUR=1\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('Reply.........' + (str(tmp))[-7:-5] + '\r\n' + '\r\n')
					break

		uart6.write('AT+CWJAP_CUR=\"TP-LINK_HW\",\"25689124\"\r\n')
		uart4.write('Connecting to.........\"TP-LINK_HW\",\"25689124\"\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('Reply.........' + (str(tmp))[-7:-5] + '\r\n' + '\r\n')
					break

		uart6.write('AT+CIPMUX=1\r\n')
		uart4.write('Sending......... AT+CIPMUX=1\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('Reply.........'+(str(tmp))[-7:-5]+'\r\n'+'\r\n')
					break

		uart6.write('AT+CIPSERVER=1,8888\r\n')
		uart4.write('Sending......... AT+CIPSERVER=1,8888\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('Reply.........'+(str(tmp))[-7:-5]+'\r\n'+'\r\n')
					break

		uart6.write('AT+CIFSR\r\n')
		uart4.write('Sending.........  AT+CIFSR\r\n')
		while 1:
			if uart6.any():
				tmp = uart6.read()
				if (str(tmp))[-7:-5]=='OK':
					uart4.write('IP.........'+(str(tmp))[30:43]+'\r\n')  # .......O
					uart4.write('Reply.........'+(str(tmp))[-7:-5]+'\r\n'+'\r\n')
					break

		uart4.write('sta mode is ready.........\r\n')


		while 1:
			if uart6.any():
				tmp = uart6.read()
				if str(tmp)[-6:-1] == 'ledOn':
					pyb.LED(3).on()
				if str(tmp)[-7:-1] == 'ledOff':
					pyb.LED(3).off()
				#uart4.write(str(tmp)[-6:-1]+'\r\n\r\n')





