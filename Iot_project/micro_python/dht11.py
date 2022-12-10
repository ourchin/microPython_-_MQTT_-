import pyb
from pyb import Pin
import time

class DHT11():
    def __init__(self, dht_pin):
        self.dht = Pin(dht_pin, Pin.OPEN_DRAIN, Pin.PULL_UP)

    def start(self):
        self.dht(0)
        time.sleep_ms(30)
        self.dht(1)
        while 1:
            if self.dht.value() == 0:
                pyb.LED(4).on()
                break

        while 1:
            if self.dht.value() == 1:
                break

        while 1:
            if self.dht.value() == 0:
                break

    def read_bytes(self, dataread):
        byteread = 0
        self.start()
        for j in range(5):
            for i in range(8):
                while 1:
                    if self.dht.value() == 1:
                        break
                time.sleep_us(30)
                if self.dht.value():
                    flag = 1
                    while 1:
                        if self.dht.value() == 0:
                            break
                else:
                    flag = 0
                byteread <<= 1
                byteread |= flag
            dataread[j] = byteread
            byteread = 0










