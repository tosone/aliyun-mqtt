import mqtt
from thunder_sdk.constants.misc import *


class Aliyun(object):

    def __init__(self, key):
        self.deviceId = key.get("deviceId")
        self.deviceSecret = key.get("deviceSecret")
        self.productKey = key.get("productKey")
        self.productSecret = key.get("productSecret")
        self.authAddress = ALIYUN_IOT_HOST
        self.client = None

    def connect(self):
        return mqtt.connect(self.authAddress, self.productKey, self.productSecret, self.deviceId, self.deviceSecret)
