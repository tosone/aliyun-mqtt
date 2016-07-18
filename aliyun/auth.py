import base64

import requests

import getHash


def getCert(authAddress, appKey, appSecret, deviceId, deviceSecret):
  params = getHash.signParams(appKey, appSecret, deviceId, deviceSecret)
  response = requests.get(authAddress, params)
  res = response.json()
  pubkey = base64.b64decode(res.get("pubkey"))
  host = res.get("servers").split(":")[0]
  port = res.get("servers").split(":")[1].split("|")[0]
  file = open("key.pem", "w+")
  file.write(pubkey)
  file.close()
  return {
      "host": host,
      "port": port
  }
