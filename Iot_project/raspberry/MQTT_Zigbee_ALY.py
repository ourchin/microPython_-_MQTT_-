# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import hashlib
import hmac
import random
import json
import serial
import time
#这个就是我们在阿里云注册产品和设备时的三元组啦
#把我们自己对应的三元组填进去即可
options = {
    'productKey':'i0avmVIZ8G3',
    'deviceName':'sensor01',
    'deviceSecret':'77daeb6b358ebf1b1db94d8ab467599c',
    'regionId':'cn-shanghai'
}

HOST = options['productKey'] + '.iot-as-mqtt.'+options['regionId']+'.aliyuncs.com'
PORT = 1883
PUB_TOPIC = "/sys/" + options['productKey'] + "/" + options['deviceName'] + "/thing/event/property/post";


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("the/topic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def hmacsha1(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha1).hexdigest()

def getAliyunIoTClient():
        timestamp = str(int(time.time()))
        CLIENT_ID = "paho.py|securemode=3,signmethod=hmacsha1,timestamp="+timestamp+"|"
        CONTENT_STR_FORMAT = "clientIdpaho.pydeviceName"+options['deviceName']+"productKey"+options['productKey']+"timestamp"+timestamp
        # set username/password.
        USER_NAME = options['deviceName']+"&"+options['productKey']
        PWD = hmacsha1(options['deviceSecret'],CONTENT_STR_FORMAT)
        client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
        client.username_pw_set(USER_NAME, PWD)
        return client


if __name__ == '__main__':
        #ser = serial.Serial("/dev/ttyAMA0", 115200)
        # 位置2：先清空缓冲区域，省得有垃圾数据没有被接收影响我们的工作
    #ser.flushInput()

    client = getAliyunIoTClient()
    client.on_connect = on_connect
    client.on_message = on_message
    print("ok")
    client.connect(HOST, 1883, 300)

    while True:
        time.sleep(1)
        ser = serial.Serial("/dev/ttyAMA0", 115200,timeout = 0.5)
        recv = []
        copy = []
        x=1
        y=1

        yy=""
        getbytes = b''
        while True:
            count = ser.inWaiting()
            if count > 0:
                data = ser.read(count)
                if data != getbytes:
                    print(data)
                    getbytes = data
                    s = getbytes.decode(encoding='utf-8')
                    # copy = s.split()
                    recv.extend(data)
                   # recv = copy.split()
                    print(recv)
                    if len(recv) > 4:
                        temperature_bit1 = recv[2:3]
                        temperature_bit2 = recv[3:4]
                        humidity_bit1 = recv[0:1]
                        humidity_bit2 = recv[1:2]
                        print(temperature_bit1)

                        x1= "".join(map(str, temperature_bit1))
                        x2= "".join(map(str, temperature_bit2))
                        y1= "".join(map(str, humidity_bit1))
                        y2= "".join(map(str, humidity_bit2))

                       # xx = ''.join(temperature_bit)
                       # yy = ''.join(humidity_bit)
                        temperature = float(x1)-float(x2)/10.0
                        humidity =  float(y1)-float(y2)/10.0
                        print(temperature)
                        print(humidity)
                        recv=[]
                        time.sleep(1)
                        if temperature!=0 or humidity!=0:
                                       payload_json = {
                                                       'id': int(time.time()),
                                                       'params': {
                                                       'humidity':   humidity,
                                                       'temperature':  temperature,
                                                      },
                                                      'method': "thing.event.property.post"
                                                      }
                                       print('send data to iot server: ' + str(payload_json))
                                       #client.publish(topic, payload=str(payload_json))
                                       client.publish(PUB_TOPIC,payload=str(payload_json),qos=1)


'''
        while True:
        # 位置4：得到当前未接收的数据有多少个
          count = ser.inWaiting()
          if count != 0:
            # 位置5：将这么多数据全部读取出来。
            recv = ser.read(count)
            print(recv)
            print("n++")
            # 位置6、7：回显接收的数据。因为接收的也是字节流，所以不需要编码，直接就能发送出去
            # ser.write("Recv some data is : ".encode("utf-8"))  # 位置6
            # ser.write(recv)  # 位置7
            ser.flushInput()
          time.sleep(0.1)  # 位置8

          payload_json = {
                'id': int(time.time()),
                'params': {
                        'temperature': random.randint(20, 30),#随机温度
                         'humidity': random.randint(30, 90)#随机相对湿度
                },
            'method': "thing.event.property.post"
         }
          print('send data to iot server: ' + str(payload_json))

          client.publish(PUB_TOPIC,payload=str(payload_json),qos=1)
          client.loop_forever()

'''
