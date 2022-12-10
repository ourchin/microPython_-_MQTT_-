
#***************************************************************
#文件名		: main.c
#作者	  	: Tao
#版本	   	: V1.0
#描述	   	: 采集温湿度，用Zigbee传输数据，并控制开关灯
#其他	   	: None
#日志	   	: V1.0 
#***************************************************************

from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块

from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块

from dht11 import DHT11

from pyb import UART

from pyb import LED



import time



i2c = I2C(sda=Pin("Y10"), scl=Pin("Y9"))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c


led1 = LED(1)
led2 = LED(2)


#初始化zigbee串口
uart = UART(6,115200)
uart.init(115200,bits=8,parity=None,stop=1)


#初始化与PC串口
uart2 = UART(4,115200)
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
print(resultList)

def up_val():
  print("ok")
  DHT11.read_bytes(resultList)
  time.sleep_ms(300)
  cmd_list[6:11]=resultList
  #uart.write("Recv some data is : ".encode("utf-8"))  # 位置6
  for dat in cmd_list:
    uart.writechar(dat)
    #uart2.writechar(dat)
    print(dat,end="")
    print(',',end="")
  print(resultList)


while True:

    if(uart.any()):

      str = uart.readline();

      print(str);

      cmd = str.decode('utf-8');
      if(str ==b'\x11'):
          print("LED1 On")
          led1.on()
      elif(str ==b'\x00'):
          print("LED1 Off")
          led1.off()
      elif(str ==b'\x22'):
          print("dht11 data reading")
          DHT11.read_bytes(resultList)
          time.sleep_ms(300)
          cmd_list[6:11]=resultList
          #uart.write("Recv some data is : ".encode("utf-8"))  # 位置6
          for dat in cmd_list:
            uart.writechar(dat)
            #uart2.writechar(dat)
            print(dat,end="")
            print(',',end="")
          print(resultList)
      else:
          print("Unknow command")


  








