const asyncMod = require('async');
const urlParser = require('url');
const URLSearchParams = require('url').URLSearchParams;
const shortid = require('shortid');
const request = require('request');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const sqs = new AWS.SQS({region: process.env.REGION});
const images = require('./images');

// retrieve domai from url
function createUniqueDomain (url) {
  'use strict';
  const parsed = urlParser.parse(url);
  const sp = new URLSearchParams(parsed.search);
  let domain;

  if (sp.get('q')) {
    domain = sp.get('q') + '.' + parsed.hostname;
  } else {
    domain = shortid.generate() + '.' + parsed.hostname;
  }
  domain = domain.replace(/ /g, '');
  return domain.toLowerCase();
}

// write status and upload status file
function writeStatus (url, domain, results) {
  'use strict';
  let parsed = urlParser.parse(url);
  parsed.hostname = domain;
  parsed.host = domain;
  const statFile = {
    url: urlParser.format(parsed),
    stat: 'downloaded',
    downloadResults: results
  };

  return new Promise((resolve) => {
    s3.putObject({
      Bucket: process.env.DATA_BUCKET,
      Key: domain + '/status.json',
      Body: Buffer.from(JSON.stringify(statFile, null, 2), 'utf8')
    }, (err, data) => {
      resolve({stat: err || 'ok'});
    });
  });
}

// crawl and fetch image
function crawl (domain, url, context) {
  'use strict';
  console.log('crawling: ' + url);
  return new Promise(resolve => {
    request(url, (err, response, body) => {
      if (err || response.statusCode !== 200) {
        return resolve({statusCode: 500, body: err}); 
      }
      images.parseImageUrls(body, url).then(urls => {
        images.fetchImages(urls, domain).then(results => {
          writeStatus(url, domain, results).then(result => {
            resolve({statusCode: 200, body: JSON.stringify(result)});
          });
        });
      });
    });
  });
}

// send a job to analysis queue
function queueAnalysis (domain, url, context) {
  'use strict';
  let accountId = process.env.ACCOUNTID;
  if (!accountId) {
    accountId = context.invokedFunctionArn.split(':')[4];
  }

  let queueUrl = `https://sqs.${process.env.REGION}.amazonaws.com/${accountId}/${process.env.ANALYSIS_QUEUE}`;

  let params = {
    MessageBody: JSON.stringify({action: 'analyze', msg: {domain: domain}}),
    QueueUrl: queueUrl
  };

  return new Promise(resolve => {
    sqs.sendMessage(params, (err, data) => {
      if (err) { 
        console.log('QUEUE ERROR: ' + err);
        return resolve({statusCode: 500, body: err});
      }
      console.log('queued analysis: ' + queueUrl);
      resolve({statusCode: 200, body: {queue: queueUrl, msgId: data.MessageId}});
    });
  });
}

// crawl each url for images
function crawlImages (event, context, cb) {
  'use strict';
  asyncMod.eachSeries(event.Records, (record, asyncCb) => {
    let { body } = record;

    try {
      body = JSON.parse(body);
    } catch (exp) {
      return asyncCb('message parse error: ' + record);
    }

    if (body.action === 'download' && body.msg && body.msg.url) {
      const uDomain = createUniqueDomain(body.msg.url);
      crawl(uDomain, body.msg.url, context).then(result => {
        queueAnalysis(uDomain, body.msg.url, context).then(result => {
          asyncCb(null, result);
        });
      });
    } else {
      asyncCb('malformed message');
    }
  }, (err) => {
    if (err) { 
      console.log(err);
    }
    cb();
  });
}

module.exports = {
  crawlImages
};