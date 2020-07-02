const urlParser = require('url');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const sqs = new AWS.SQS({region: process.env.REGION});

// create response for a HTTP request
function respond (code, body, cb) {
  'use strict';
  const response = {
    statusCode: code,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true
    },
    body: JSON.stringify(body)
  };
  console.log(JSON.stringify(response));
  cb(null, response);
}

// read 'status.json' file into an object
function readStatus (folder) {
  'use strict';
  const params = {
    Bucket: process.env.DATA_BUCKET,
    Key: folder + 'status.json'
  };
  console.log(JSON.stringify(params, null, 2));
  return new Promise((resolve) => {
    s3.getObject(params, (err, data) => {
      if (err) {
        return resolve({stat: err});
      }
      let statFile = JSON.parse(data.Body.toString());
      resolve(statFile);
    });
  });
}

// given url, create and send images download action
function analyzeUrl (event, context, cb) {
  'use strict';
  let accountId = process.env.ACCOUNTID;
  if (!accountId) {
    accountId = context.invokedFunctionArn.split(':')[4];
  }
  const queueUrl = `https://sqs.${process.env.REGION}.amazonaws.com/${accountId}/${process.env.QUEUE}`;
  const body = JSON.parse(event.body);

  const params = {
    MessageBody: JSON.stringify({action: 'download', msg: body}),
    QueueUrl: queueUrl
  };

  console.log('analyze url');
  console.log(JSON.stringify(params, null, 2));

  sqs.sendMessage(params, (err, data) => {
    if (err) {
      return respond(500, {
        stat: 'error',
        details: err
      }, cb);
    }
    respond(200, {
      stat: 'ok',
      details: {
        queue: queueUrl,
        msgId: data.MessageId
      }
    }, cb);
  });
}

// list submitted urls and their status
function listUrls (event, context, cb) {
  'use strict';
  const params = {
    Bucket: process.env.DATA_BUCKET,
    Delimiter: '/',
    MaxKeys: 1000
  };

  console.log('list urls');
  s3.listObjectsV2(params, (err, data) => {
    let promises = [];
    if (err) {
      return respond(500, {
        stat: 'error',
        details: err
      }, cb);
    }

    data.CommonPrefixes.forEach(prefix => {
      promises.push(readStatus(prefix.Prefix));
    });

    Promise.all(promises).then(values => {
      let results = [];
      values.forEach(value => {
        results.push({
          url: value.url,
          stat: value.stat
        });
      });
      respond(200, {
        stat: 'ok', 
        details: results
      }, cb);
    });
  });
}

// list downloaded images and their status
function listImages (event, context, cb) {
  'use strict';
  const url = event.queryStringParameters.url;
  const domain = urlParser.parse(url).hostname;

  console.log('list images');
  readStatus(domain + '/').then(result => {
    respond(200, {
      stat: 'ok', 
      details: result
    }, cb);
  });
}

// entry points
module.exports = {
  analyzeUrl,
  listUrls,
  listImages
};
