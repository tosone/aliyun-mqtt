from aliyun import *
from device import *
import paho.mqtt.publish as publish
import redis
import json, time

def innerMq(topic, payload):
  publish.single(topic, payload, hostname = "127.0.0.1", port = 1883)

def onMessage(client, userdata, msg):
  payload = json.loads(msg.payload.replace("'", "\""))
  innerMq(payload.get("deviceTopic"), json.dumps(payload.get("payload")))
  print(msg.topic + " " + str(msg.payload))
  
def onConnect(client, userdata, flags, rc):  
  payload = {
    "deviceTopic": "test-cloud-gateway",
    "payload":{
      "corelationId": "d2eb3ac4-1174-4368-b8d9-19c5f06848b5",
      "address": "http://baidu.com/test-cloud-gateway"
    }
  }
  client.publish("23390947/devices/" + mac.get(), json.dumps(payload))
  print("AliyunIot Connected with result code " + str(rc))

def mqttConfig():
  try:
    mqttClient = aliyun.connect()
    mqttClient.on_message = onMessage
    mqttClient.on_connect = onConnect
    print mac.get()
    mqttClient.subscribe("23390947/devices/" + mac.get())
    print "23390947/devices/" + mac.get()
    mqttClient.loop_forever()
  except:
    print "except with err after 3s will restart."
    time.sleep(3)
    mqttConfig()

appKey = "23390947"
appSecret = "3ebb2e6c5034a1c496feba1f3c1d23c7"

r = redis.StrictRedis(host='localhost', port=6379, db=6)
while True:
  if(r.get("deviceId") is not None and r.get("deviceSecret") is not None):
    if(net.isConnected() or net.continueTest()):
      aliyun = aliyun.Aliyun({"deviceId": r.get("deviceId"), "deviceSecret": r.get("deviceSecret"), "appKey": appKey, "appSecret": appSecret})
      mqttConfig()
      break
  else:
    print "redis has no key about device."
    time.sleep(3)
    continue
