from dht11 import DHT11
from pyb import UART
from pyb import LED
import time

uart2 = UART(4,115200)
led1 = LED(1)
led2 = LED(2)
uart2.write("please enter led command:\n\r")


#初始化串口
uart = UART(6,115200)
uart.init(115200,bits=8,parity=None,stop=1)
#zigbee：向短ip 00 00发送信息,发送9位，点播1透传
cmd_list=[0xFC,0x09,0x03,0x01,0x00,0x00,0x31,0x32,0x33,0x34,0x35]

#DHTT11采集列表，第5位为校验和
DHT11 = DHT11('B13')
resultList = [0, 0, 0, 0, 0]

count = 0

# DHT11采集数据

while True:
    if(uart2.any()):
      str = uart2.readline();
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
      elif(cmd == "read dht11 data"):
          print("dht11 data reading")
          DHT11.read_bytes(resultList)
          time.sleep_ms(300)
          cmd_list[6:11]=resultList
          for dat in cmd_list:
            uart.writechar(dat)
          print(resultList)
      else:
          print("Unknow command")



'''
while True:
  
  count += 1;
  DHT11.read_bytes(resultList)
  time.sleep_ms(500)
  cmd_list[6:11]=resultList
  for dat in cmd_list:
    uart.writechar(dat) 
  

  print(" humity: ",end="")
  print(str(resultList[0]),end="")
  print(".",end="")
  print(str(resultList[1]))
  
  print(" tempeture: ",end="")
  print(str(resultList[2]),end="")
  print(".",end="")
  print(str(resultList[3]))

  
  print(resultList)
  print(count)
  #pyb.delay(500)
  time.sleep_ms(500)
'''



