#!/usr/bin/env python

import paho.mqtt.client as mqtt
import requests

import hashlib
import hmac

BROKER_ADDRESS = "127.0.0.1"
ALIYUN_AUTH_ADDRESS = "http://manager.channel.aliyun.com/iot/auth"

ALIYUN_APP_ID = "appid"
ALIYUN_APP_SECRET = "secret"

TOPIC_INTERNET_CONNECTED = "hook/network/internetconnected"

STORE_MANIFEST = 3

manifest_store = None
device_client = None
aliyun_client = None

def handle_internet_connected():
    if not aliyun_connected:
        aliyun_connect()

def handle_aliyun_message(payload):
    global device_client
    data = json.loads(payload)
    device.publish(data.topic, data.payload)

def aliyun_create_auth_params(app_key, app_secret, device_id, device_secret):
    data = "appKey" + app_key + "deviceId" + device_id
    secret = app_secret + device_secret
    hmac_object = hmac.new(secret)
    hmac_object.update(data)
    return {
        deviceId: device_id,
        appKey: app_key,
        sign: hmac_object.hexdigest().upper()
    }

def aliyun_create_username(app_key, app_secret, device_id, device_secret):
    data = app_key + app_secret + device_id + device_secret
    md5_object = hashlib.md5()
    md5_object.update(data)
    return md5_object.hexdigest().upper()

def aliyun_resolve_auth_info(response_data):
    pubkey = "pubkey"
    server_info = response_data.servers.split(":")
    host = server_info[0]
    port = server_info[1].split("|")
    return {
        pubkey: pubkey,
        host: host,
        port: port
    }

def aliyun_auth(app_key, app_secret, device_id, device_secret):
    params = aliyun_create_auth_param(app_key, app_secret, device_id, device_secret)
    response = requests.get(ALIYUN_AUTH_ADDRESS, params = params)
    return resolve_aliyun_auth_info(response.json())

def aliyun_connect():
    global aliyun_client

    app_key = ALIYUN_APP_KEY
    app_secret = ALIYUN_APP_SECRET
    device_id = manifest_store.get("aliyunDeviceId")
    device_secret = manifest_store.get("aliyunDeviceSecret")

    server_info = aliyun_auth()
    client_id = app_key + ":" device_id
    username = aliyun_create_username(app_key, app_secret, device_id, device_secret)

    aliyun_client = mqtt.Client(client_id)
    aliyun_client.on_connect = on_aliyun_connect
    aliyun_client.on_message = on_aliyun_message
    aliyun_client.tls_set(certfile = server_info.pubkey)
    aliyun_client.tls_insecure_set(True)
    aliyun_client.username_pw_set(username)
    aliyun_client.connect(server_info.host, server_info.port)

def create_device_topic():
    return ALIYUN_APP_ID + "/devices/" + get_mac_address()

def get_mac_address():
    # TODO check if need to select interface
    import uuid, re
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def on_device_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe(TOPIC_INTERNET_CONNECTED)

def on_aliyun_connect(client, userdata, flags, rc):
    print("connect to aliyun " + stc(rc))
    client.subscribe(create_device_topic())

def on_device_message(client, userdata, msg):
    if msg.topic == TOPIC_INTERNET_CONNECTED:
        return handle_internet_connected(msg.payload)

def on_aliyun_message(client, userdata, msg):
    handle_aliyun_message(msg.payload)

def main():
    global device_client
    global manifest_store

    manifest_store = redis.StrictRedis(db = STORE_MANIFEST)

    device_client = mqtt.Client()
    device_client.on_connect = on_device_connect
    device_client.on_message = on_device_message
    device_client.connect(BROKER_ADDRESS)

    device_client.loop_forever()

if __name__ == "__main__":
    main()
