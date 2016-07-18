import socket
import time

REMOTE_SERVER = "www.baidu.com"


def isConnected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
    pass
  return False


def continueTest():
  while True:
    if(isConnected()):
      return True
      break
    else:
      print "Device is not online.[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]"
      time.sleep(10)
      continue
