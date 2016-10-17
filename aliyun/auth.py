import base64

import requests

import config
import getHash


def getCert(authAddress, appKey, appSecret, deviceId, deviceSecret):
    params = getHash.signParams(appKey, appSecret, deviceId, deviceSecret)
    response = requests.get(authAddress, params)
    res = response.json()
    pubkey = base64.b64decode(res.get("pubkey"))
    host = res.get("servers").split(":")[0]
    port = res.get("servers").split(":")[1].split("|")[0]
    file = open(config.definition().get("KEY_PEM_FILE"), "w+")
    file.write(pubkey)
    file.close()
    return {
        "host": host,
        "port": port
    }
