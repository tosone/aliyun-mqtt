import os.path
import ssl

import paho.mqtt.client as mqtt
import redis

import auth
import getHash


def connect(authAddress, appKey, appSecret, deviceId, deviceSecret):
  keyfile = "key.pem"
  r = redis.StrictRedis(host='localhost', port=6379, db=6)
  if(r.get("host") is None or r.get("host") is None or not os.path.isfile(keyfile)):
    res = auth.getCert(authAddress, appKey, appSecret, deviceId, deviceSecret)
    r.set("host", res.get("host"))
    r.set("port", res.get("port"))
  host = r.get("host")
  port = r.get("port")
  client_id = appKey + ":" + deviceId
  username = getHash.username(appKey, appSecret, deviceId, deviceSecret)
  client = mqtt.Client(client_id=client_id,
                       clean_session=True,  protocol="MQTTv311")
  client.tls_set(keyfile, cert_reqs=ssl.CERT_NONE,
                 tls_version=ssl.PROTOCOL_TLSv1_1)
  client.tls_insecure_set(True)
  client.username_pw_set(username)
  client.connect(host,  port=int(port), keepalive=120)
  return client
