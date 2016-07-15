# Aliyun iot-mqtt

### Package
- `pip install paho-mqtt`
- `pip install requests`
- `pip install redis`

### Step
- `sudo apt install mosquitto`

### Test
- Add redis keys
```
select 6
set deviceId 0RWmNAYUMEJmwNc2R
set deviceSecret u2PDAhO6JjYPdmA1
```
- test: `python test.py`
- get: `python get.py`

### TODO
- Test device is online or not with bbcloud.

### Redis DB6 keys
- deviceKey
- deviceSecret
- host
- port

### Notice
- AliyunIot is unidirectional authentication, that you should set maho tls  cert_reqs is ssl.CERT_NONE.
- You should subscribe a topic after connect mq server.

### Old Version
- `sudo apt install rabbitmq-server`
- `sudo rabbitmq-plugins enable rabbitmq_mqtt`
- Rabbit's default mq is AMQP, its port is 5672, you should enable mqtt as above, and its default port is 1883.
