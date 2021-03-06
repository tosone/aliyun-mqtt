import os.path
import ssl
import threading

import paho.mqtt.client as mqtt
import redis

import auth
import config
import getHash
import net
from thunder_sdk.services.storage import config_store


def connect(authAddress, appKey, appSecret, deviceId, deviceSecret):
    keyfile = config.definition().get("KEY_PEM_FILE")
    AliyunHost = "AliyunIotHost"
    AliyunPort = "AliyunIotPort"
    if config_store.get(AliyunHost) is None or config_store.get(AliyunPort) is None or not os.path.isfile(keyfile):
        res = auth.getCert(authAddress, appKey, appSecret, deviceId, deviceSecret)
        config_store.set(AliyunHost, res.get("host"))
        config_store.set(AliyunPort, res.get("port"))
    host = config_store.get(AliyunHost)
    port = config_store.get(AliyunPort)
    client_id = appKey + ":" + deviceId
    username = getHash.username(appKey, appSecret, deviceId, deviceSecret)
    client = mqtt.Client(client_id=client_id, clean_session=True, protocol="MQTTv311")
    client.tls_set(keyfile, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_1)
    client.tls_insecure_set(True)
    client.username_pw_set(username)
    client.connect(host,  port=int(port))

    def check_connected_iot():
        if net.continueTestNotOnline():
            client.reconnect()
    thread = threading.Thread(target=check_connected_iot, args=())
    thread.start()

    return client
