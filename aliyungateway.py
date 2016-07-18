#!/usr/bin/env python

import json
import time

import paho.mqtt.publish as publish
import redis

from aliyun import *

appKey = "23360505"
appSecret = "db1336ffcb784668302927979e7eeb77"
redisHost = 'localhost'
redisPort = 6379
redisDB = 6
mqttHost = "192.168.1.3"
mqttPort = 1883

r = redis.StrictRedis(host=redisHost, port=redisPort, db=redisDB)

r.set("deviceId", "0RWmNAYUMEJmwNc2R")
r.set("deviceSecret", "u2PDAhO6JjYPdmA1")

CONFIG = {
    "deviceId": r.get("deviceId"),
    "deviceSecret": r.get("deviceSecret"),
    "appKey": appKey,
    "appSecret": appSecret
}


def innerMq(topic, payload):
  publish.single(topic, payload, hostname=mqttHost, port=mqttPort)


def onMessage(client, userdata, msg):
  # print(msg.topic + " " + str(msg.payload))
  try:
    payload = json.loads(msg.payload.replace("'", "\""))
  except:
    print "AliyunIotGateway: receive error schema msg."
  innerMq(payload.get("deviceTopic"), json.dumps(payload.get("payload")))
  # print(msg.topic + " " + str(payload))


def onConnect(client, userdata, flags, rc):
  # payload = {
  #     "deviceTopic": "test-cloud-gateway",
  #     "payload": {
  #         "corelationId": "d2eb3ac4-1174-4368-b8d9-19c5f06848b5",
  #         "address": "http://baidu.com/test-cloud-gateway"
  #     }
  # }
  # client.publish(appKey + "/devices/00:00:00:00:00:00", json.dumps(payload))
  print("AliyunIot Connected with result code " + str(rc))


def mqttConfig():
  try:
    mqttClient = aliyun.connect()
    mqttClient.on_message = onMessage
    mqttClient.on_connect = onConnect
    mqttClient.subscribe(appKey + "/devices/00:00:00:00:00:00")
    mqttClient.loop_forever()
  except:
    print "AliyunIotGateway: Except with err after 3s will restart."
    time.sleep(3)
    mqttConfig()


while True:
  if r.get("deviceId") is not None and r.get("deviceSecret") is not None:
    if(net.isConnected() or net.continueTest()):
      aliyun = aliyun.Aliyun(CONFIG)
      mqttConfig()
      break
  else:
    print "AliyunIotGateway: Redis has no key about device."
    time.sleep(3)
    continue
