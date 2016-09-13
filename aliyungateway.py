#!/usr/bin/env python

import json
import time

import paho.mqtt.publish as publish

from aliyun import *
from thunder_sdk import device
from thunder_sdk.constants.misc import *
from thunder_sdk.helpers.singleton import SingleInstance
from thunder_sdk.sdks.appsconf import *

singleIns = SingleInstance(flavor_id="aliyungateway")


class AliyunCloudGateway():

    def __init__(self):
        self.interval_retry_getKey = 10
        self.interval_retry_start = 3
        self.retry = 0
        self.retry_times = 5
        # Just for test. Release will be replaced.
        # self.deviceMac = "00:00:00:00:00:00"
        self.deviceMac = device.get_mac_address()
        self.aliyun = aliyun
        self.publish = publish

    def innerMq(self, topic, payload):
        self.publish.single(topic, payload, hostname=BROKER_ADDRESS)

    def onMessage(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        try:
            payload = json.loads(msg.payload.replace("'", "\""))
            self.innerMq(payload.get("deviceTopic"), json.dumps(payload.get("payload")))
        except:
            print "AliyunCloudGateway: receive error schema msg."

    def onConnect(self, client, userdata, flags, rc):
        client.subscribe(self.productKey + "/devices/" + self.deviceMac)
        print("AliyunCloudGateway Connected with result code " + str(rc))

    def iotConn(self):
        try:
            mqttClient = self.aliyunClient.connect()
            mqttClient.on_message = self.onMessage
            mqttClient.on_connect = self.onConnect
            mqttClient.loop_forever()
        except:
            print "AliyunCloudGateway: Except with err after 3s will restart."
            time.sleep(self.interval_retry_start)
            self.retry = self.retry + 1
            if self.retry < self.retry_times:
                self.iotConn()
            else:
                print "AliyunCloudGateway: restart too many times, after 60s will retry."
                time.sleep(60)
                self.retry = 0
                self.iotConn()

    def main(self):
        while True:
            if retrieve("productKey") is not None and retrieve("productSecret") is not None:
                if retrieve("deviceId") is not None and retrieve("deviceSecret") is not None:
                    if net.isConnected() or net.continueTest():
                        self.productKey = retrieve("productKey")
                        self.productSecret = retrieve("productSecret")
                        self.deviceId = retrieve("deviceId")
                        self.deviceSecret = retrieve("deviceSecret")
                        CONFIG = {
                            "deviceId": self.deviceId,
                            "deviceSecret": self.deviceSecret,
                            "productKey": self.productKey,
                            "productSecret": self.productSecret
                        }
                        self.aliyunClient = self.aliyun.Aliyun(CONFIG)
                        self.iotConn()
                        break
                else:
                    print "AliyunCloudGateway: Redis has no info about device."
                    time.sleep(self.interval_retry_getKey)
                    continue
            else:
                print "AliyunCloudGateway: Redis has no info about product."
                time.sleep(self.interval_retry_getKey)
                continue

if __name__ == "__main__":
    aliyunCloudGateway = AliyunCloudGateway()
    aliyunCloudGateway.main()
