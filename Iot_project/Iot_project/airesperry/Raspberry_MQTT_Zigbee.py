#***************************************************************
#文件名         : iot.py
#作者           : Tao
#版本           : V1.1
#描述           :作为网关，从Zigbee获取数据上报阿里云，并接收阿里云命令传递给节点开关灯
#其他           : None
#日志           : V1.1
#***************************************************************

import json
import random
import serial
import time
import _thread
import threading
import paho.mqtt.client as mqtt
from MqttSign import AuthIfo

# set the device info, include product key, device name, and device secret
productKey = "i0avmVIZ8G3"
deviceName = "sensor01"
deviceSecret = "77daeb6b358ebf1b1db94d8ab467599c"

# set timestamp, clientid, subscribe topic and publish topic
timeStamp = str((int(round(time.time() * 1000))))
clientId = "12345"
subTopic = "/sys/" + productKey + "/" + deviceName + "/thing/service/property/set"
pubTopic = "/sys/" + productKey + "/" + deviceName + "/thing/event/property/post"
# set host, port
host = "i0avmVIZ8G3.iot-as-mqtt.cn-shanghai.aliyuncs.com"
# instanceId = "***"
# host = instanceId + ".mqtt.iothub.aliyuncs.com"
port = 1883

# set tls crt, keepalive
tls_crt = "root.crt"
keepAlive = 300

# calculate the login auth info, and set it into the connection options
m = AuthIfo()
m.calculate_sign_time(productKey, deviceName, deviceSecret, clientId, timeStamp)
client = mqtt.Client(m.mqttClientId)
client.username_pw_set(username=m.mqttUsername, password=m.mqttPassword)
client.tls_set(tls_crt)

ser = serial.Serial("/dev/ttyAMA0", 115200,timeout = 0.5)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect aliyun IoT Cloud Sucess")
    else:
        print("Connect failed...  error code is:" + str(rc))

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print("receive message ---------- topic is : " + topic)
    print("receive message ---------- payload is : " + payload)
    print("*******接受消息************")
    print("下发命令:" + str(msg.payload, 'utf-8') + "°C")
   # cmd = str(msg.payload, 'utf-8')
   # Msg=json.loads(msg.payload)
   # global lightswitch
   # lightswitch=Msg['params']['LightSwitch']
   # print("lightswitch value:",end='')
   # print(lightswitch)
   # print(cmd)
    if ("thing/service/property/set" in topic):
        on_thing_prop_changed(client, msg.topic, msg.payload)

def  led_on():
     ser.write(b'\xFC\x03\x02\x01\x11')

def  led_off():
    ser.write(b'\xFC\x03\x02\x01\x00')

def  read_data():
   while True:
        ser.write(b'\xFC\x03\x02\x01\x22')
        time.sleep(10)

def on_thing_prop_changed(client, topic, payload):

    Msg=json.loads(payload)
    global lightswitch
    lightswitch=Msg['params']['LightSwitch']
    print("lightswitch value:",end='')
    print(lightswitch)
    if(lightswitch):
           led_on()
           print("led on")
    if(lightswitch==0):
           led_off()
           print("led off")

    post_topic = topic.replace("service","event")
    post_topic = post_topic.replace("set","post")
    params = Msg['params']
    post_payload = "{\"params\":" + json.dumps(params) + "}"
    print("reveice property_set command, need to post ---------- topic is: " + post_topic)
    print("reveice property_set command, need to post ---------- payload is: " + post_payload)
    client.publish(post_topic, post_payload)

def connect_mqtt():
    client.connect(host, port, keepAlive)
    return client

def publish_message():

   # client.on_connect = on_connect
   # client.on_message = on_message
    print("ok")
   # client.connect(HOST, 1883, 300)

    while True:
        time.sleep(1)
       # ser = serial.Serial("/dev/ttyAMA0", 115200,timeout = 0.5)
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
                        #print(temperature_bit1)

                        x1= "".join(map(str, temperature_bit1))
                        x2= "".join(map(str, temperature_bit2))
                        y1= "".join(map(str, humidity_bit1))
                        y2= "".join(map(str, humidity_bit2))

                       # xx = ''.join(temperature_bit)
                       # yy = ''.join(humidity_bit)
                        temperature = float(x1)+float(x2)/10.0
                        humidity =  float(y1)+float(y2)/10.0
                        print(" 温度:  ",temperature)
                        print(" 湿度： ",humidity)
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
                                       client.publish(pubTopic,payload=str(payload_json),qos=1)

def subscribe_topic():
    # subscribe to subTopic("/a1LhUsK****/python***/user/get") and request messages to be delivered
    client.subscribe(subTopic)
    print("subscribe topic: " + subTopic)

client.on_connect = on_connect
client.on_message = on_message
client = connect_mqtt()
client.loop_start()
time.sleep(3)
#subscribe_topic()
#publish_message()

if __name__ == '__main__':
 while True:
        t1 = threading.Thread(target=read_data, args=())
        t2 = threading.Thread(target=publish_message, args=())
        t1.start()
        t2.start()
        time.sleep(3)
        t1.join()
        t2.join()
       # time.sleep(1)
