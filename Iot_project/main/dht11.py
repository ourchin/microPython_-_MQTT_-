from dht11 import DHT11

import time

from lcd1602 import LCD1602


DHT11 = DHT11('B13')


resultList = [0, 0, 0, 0, 0]
count = 0;



# DHT11采集数据


while True:
  
  count += 1;
  DHT11.read_bytes(resultList)
  time.sleep_ms(1000)
  print(" humity: ",end="")
  print(str(resultList[0]),end="")
  print(".",end="")
  print(str(resultList[1]))
  
  print(" tempeture: ",end="")
  print(str(resultList[2]),end="")
  print(".",end="")
  print(str(resultList[3]))
  
  print(str(count))
  
  time.sleep_ms(500)




