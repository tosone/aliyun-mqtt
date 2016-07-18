import mqtt


class Aliyun(object):

  def __init__(self, key):
    self.deviceId = key.get("deviceId")
    self.deviceSecret = key.get("deviceSecret")
    self.appKey = key.get("appKey")
    self.appSecret = key.get("appSecret")
    self.authAddress = "http://manager.channel.aliyun.com/iot/auth"
    self.client = None

  def connect(self):
    return mqtt.connect(self.authAddress, self.appKey, self.appSecret, self.deviceId, self.deviceSecret)
