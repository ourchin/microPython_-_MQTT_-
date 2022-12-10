
from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块

from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块

from dht11 import DHT11

from pyb import UART

from pyb import LED

import time



i2c = I2C(sda=Pin("Y10"), scl=Pin("Y9"))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c





#初始化串口
uart = UART(6,115200)
uart.init(115200,bits=8,parity=None,stop=1)

uart2 = UART(4,115200)
led1 = LED(1)
led2 = LED(2)
uart2.write("please enter led command:\n\r")

#zigbee：向短ip 00 00发送信息,发送9位，点播1透传
cmd_list=[0xFC,0x09,0x03,0x01,0x00,0x00,0x31,0x32,0x33,0x34,0x35]



#DHTT11采集列表，第5位为校验和
print(1)
DHT11 = DHT11('B13')

resultList = [0, 0, 0, 0, 0]
print(resultList)
md=[1,2,3,4]

#print(str(md))

count = 0



# DHT11采集数据

DHT11.read_bytes(resultList)


while True:
    
    count+=1
    time.sleep_ms(1000)
    print(count)
    DHT11.read_bytes(resultList)
    
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
    oled.fill(0)
    oled.text("humity:", 0,  0)      #写入第1行内容
    oled.text(str(resultList[0])+"."+str(resultList[1]) ,60,  0)
    oled.text(str(resultList[2])+"."+str(resultList[3]) ,90, 20)
    oled.text("tempeture:",  0, 20)      #写入第2行内容

    oled.text("dht11 data",  0, 50)      #写入第3行内容

    oled.show()   #OLED执行显示
    
  