
from pyb import UART
import time
uart=UART(4,115200) #设置串口号3和波特率,TX--Y9,RX--Y10
uart.init(115200,bits=8,parity=None,stop=1)
uart.write('Hello!n')#发送一条数据
while True:
    #判断有无收到信息
    if uart.any():
        text=uart.readline() #默认单次最多接收64字节
        print(text) #通过REPL打印串口3接收的数据