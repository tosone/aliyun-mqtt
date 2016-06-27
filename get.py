import paho.mqtt.client as mqtt
import requests, json

def innerMqOnConnect(client, userdata, flags, rc):
  print("AliyunIot Connected with result code " + str(rc))

def innerMqOnMsg(client, userdata, msg):
  payload = json.loads(msg.payload)
  res = requests.get(payload.get("address"),{
    "corelationId": payload.get("corelationId")
  })
  print res

client = mqtt.Client()
client.on_connect = innerMqOnConnect
client.on_message = innerMqOnMsg
client.connect("127.0.0.1",  1883, 60)
client.subscribe("test-cloud-gateway")
client.loop_forever()