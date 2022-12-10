from pyb import UART
from pyb import LED
uart = UART(4,115200)
led1 = LED(1)
led2 = LED(2)
uart.write("please enter led command:\n\r")
while True:
    if(uart.any()):
      str = uart.readline();
      print(str);
      cmd = str.decode('utf-8');
      if(cmd == "led1 = on"):
          print("LED1 On")
          led1.on()
      elif(cmd == "led1 = off"):
          print("LED1 Off")
          led1.off()
      elif(cmd == "led2 = on"):
          print("LED2 On")
          led2.on()
      elif(cmd == "led2 = off"):
          print("LED2 Off")
          led2.off()
      else:
          print("Unknow command")
