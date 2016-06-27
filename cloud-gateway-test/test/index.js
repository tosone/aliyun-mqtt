var APP_KEY = '23390947';
var MAC_ADDRESS = '58_94_6B_86_A0_F4';

var PUBLISHER_APP_KEY = '23390947';
var PUBLISHER_APP_SECRET = '3ebb2e6c5034a1c496feba1f3c1d23c7';
var PUBLISHER_ID = '90a7c3c39dbb4c8a93755e5903169d3c';
var PUBLISHER_SECRET = '2af6c4c0591a4b238620ecf7933ecf71';

describe('cloud gate test', function() {

  this.timeout(100000);

  it('should receive message', function() {

    var appKey = APP_KEY;
    var macAddress = MAC_ADDRESS;
    var publisherAppKey = PUBLISHER_APP_KEY;
    var publisherAppSecret = PUBLISHER_APP_SECRET;
    var publisherId = PUBLISHER_ID;
    var publisherSecret = PUBLISHER_SECRET;

    return test(appKey, macAddress, publisherAppKey, publisherAppSecret, publisherId, publisherSecret);

  });

});

function test(appKey, macAddress, publisherAppKey, publisherAppSecret, publisherId, publisherSecret) {

  var address = 'http://127.0.0.1:3000/test-cloud-gateway';
  var corelationId = require('node-uuid').v4();

  var task = listenTestResult(address, corelationId);
  publishWithMQTT('test-cloud-gateway', { corelationId, address });

  return task;

  function publishWithMQTT(deviceTopic, payload) {
    var topic = `${appKey}/devices/${macAddress}`;
    var aliyuniot = require('aliyuniot');
    aliyuniot(publisherAppKey, publisherAppSecret, publisherId, publisherSecret).then(function(client) {
      console.log(topic);
      client.publish(topic, JSON.stringify({ deviceTopic, payload }));
      console.log("succ");
    });
  }

  function listenTestResult(address, corelationId) {
    var url = require('url').parse(address);
    var app = require('express')();
    var task = new Promise(function(resolve, reject) {
      app.get(url.pathname, function(req, res, next) {
        var returnId = req.query.corelationId;
        if (match(returnId, corelationId)) {
          res.json({ code: 200 });
          return resolve();
        }
        reject();
        res.status(500).json({ code: 500 });
      });
    });

    app.listen(url.port);

    return task;
  }

  function match(returnId, corelationId) {
    return returnId === corelationId;
  }

}

function publishWithOpenAPI(payload) {
  var IOT = require('waliyun').IOT;
  var topic = `${AppKey}/devices/${macAddress}`;
  var opts = { AccessKeyId, AccessKeySecret, AppKey, Version };
  var iot = new IOT(opts);
  iot.Pub({
    MessageContent: payload,
    TopicFullName: topic //`devices/${macAddress}`
  }).then(function(result) {
    console.log('send ok');
    console.log(result);
  }).catch(function() {
    console.log('send nay');
  });
}
