import pyb
import time
while True:
  pyb.LED(4).toggle()
  time.sleep_ms(1000) 
  pyb.LED(3).toggle()
  time.sleep_ms(1000)
  pyb.LED(2).toggle()
  time.sleep_ms(1000)
  pyb.LED(1).toggle()
  time.sleep_ms(1000)