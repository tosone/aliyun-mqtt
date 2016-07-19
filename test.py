import json

import paho.mqtt.client as mqtt
import requests


def innerMqOnConnect(client, userdata, flags, rc):
  print("AliyunIot Connected with result code " + str(rc))


def innerMqOnMsg(client, userdata, msg):
  print(msg.topic + " " + str(msg.payload))
  # payload = json.loads(msg.payload)
  # res = requests.get(payload.get("address"), {
  #     "corelationId": payload.get("corelationId")
  # })
  # print res

client = mqtt.Client()
client.on_connect = innerMqOnConnect
client.on_message = innerMqOnMsg
client.connect("localhost",  1883, 60)
client.subscribe("apps_configuration/modify/request")
client.loop_forever()
