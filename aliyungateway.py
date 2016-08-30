#!/usr/bin/env python

import json
import time

import paho.mqtt.publish as publish
import redis

from aliyun import *
from thunder_sdk.helpers.singleton import SingleInstance
from thunder_sdk.constants.misc import *

singleIns = SingleInstance(flavor_id="aliyungateway")

appKey = "23390947"
appSecret = "3ebb2e6c5034a1c496feba1f3c1d23c7"

redisHost = BROKER_ADDRESS
redisPort = 6379
redisDB = 6

mqttHost = BROKER_ADDRESS
mqttPort = 1883

r = redis.StrictRedis(host=redisHost, port=redisPort, db=redisDB)

r.set("deviceId", "90a7c3c39dbb4c8a93755e5903169d3c")
r.set("deviceSecret", "2af6c4c0591a4b238620ecf7933ecf71")

CONFIG = {
    "deviceId": r.get("deviceId"),
    "deviceSecret": r.get("deviceSecret"),
    "appKey": appKey,
    "appSecret": appSecret
}


def innerMq(topic, payload):
  publish.single(topic, payload, hostname=mqttHost, port=mqttPort)


def onMessage(client, userdata, msg):
  print(msg.topic + " " + str(msg.payload))
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
