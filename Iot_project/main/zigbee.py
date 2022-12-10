uart = UART(6,115200)
uart.init(115200,bits=8,parity=None,stop=1)
#向短ip 00 00发送信息,发送8位，点播1透传
cmd_list=[0xFC,0x08,0x03,0x01,0x00,0x00,0x31,0x32,0x33,0x34]
count=0

#cmd_list[6:10]=[0x77,0x77,0x77,0x77]
print(cmd_list)
while True:
  count+=1
  for dat in cmd_list:
    uart.writechar(dat) 
  pyb.delay(1000)
  print(count)