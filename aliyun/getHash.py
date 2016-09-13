import hashlib
import hmac


def signParams(appKey, appSecret, deviceId, deviceSecret):
    data = "appKey" + appKey + "deviceId" + deviceId
    secret = appSecret + deviceSecret
    hmac_object = hmac.new(secret)
    hmac_object.update(data)
    return {
        "deviceId": deviceId,
        "appKey": appKey,
        "sign": hmac_object.hexdigest().upper()
    }


def username(appKey, appSecret, deviceId, deviceSecret):
    data = appKey + appSecret + deviceId + deviceSecret
    md5_object = hashlib.md5()
    md5_object.update(data)
    return md5_object.hexdigest().upper()
