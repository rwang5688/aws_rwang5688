const asyncMod = require('async');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const rek = new AWS.Rekognition();

// call Amazon Rekognition to detect image labels
function analyzeImageLabels (imageBucketKey) {
  'use strict';
  const params = {
    Image: {
      S3Object: {
        Bucket: process.env.DATA_BUCKET,
        Name: imageBucketKey
      }
    },
    MaxLabels: 10,
    MinConfidence: 80
  };

  return new Promise((resolve, reject) => {
    rek.detectLabels(params, (err, data) => {
      if (err) { 
        return resolve({
          image: imageBucketKey, 
          labels: [], 
          err: err}); 
      }
      return resolve({
        image: imageBucketKey,
        labels: data.Labels});
    });
  });
}

// create word cloud list from labels
function createWordCloudList (labels) {
  'use strict';
  let counts = {};
  let wcList = [];

  labels.forEach(set => {
    set.labels.forEach(lab => {
      if (!counts[lab.Name]) {
        counts[lab.Name] = 1;
      } else {
        counts[lab.Name] = counts[lab.Name] + 1;
      }
    });
  });

  Object.keys(counts).forEach(key => {
    wcList.push([key, counts[key]]);
  });
  return wcList;
}

// write analysis status, labels, and word cloud list
function writeAnalysisResults (domain, labels, wcList) {
  'use strict';
  return new Promise((resolve) => {
    var params = {
      Bucket: process.env.DATA_BUCKET,
      Key: domain + '/status.json'
    };

    s3.getObject(params, (err, data) => {
      if (err) {
        return resolve({stat: err});
      }
      let statFile = JSON.parse(data.Body.toString());
      statFile.stat = 'analyzed';
      statFile.analysisResults = labels;
      statFile.wordCloudList = wcList;
      s3.putObject({
        Bucket: process.env.DATA_BUCKET,
        Key: domain + '/status.json',
        Body: Buffer.from(JSON.stringify(statFile, null, 2), 'utf8')}, (err, data) => {
          resolve({stat: err || 'ok'});
        });
    });
  });
}

// analyze all images in the bucket
function iterateBucket (domain) {
  'use strict';
  let promises = [];
  const params = {
    Bucket: process.env.DATA_BUCKET,
    Prefix: domain,
    MaxKeys: 1000
  };

  return new Promise(resolve => {
    s3.listObjectsV2(params, (err, data) => {
      if (err) {
        return resolve({statusCode: 500, body: JSON.stringify(err)}); 
      }
      
      data.Contents.forEach(imageFile => {
        if (imageFile.Key !== domain + '/status.json') {
          promises.push(analyzeImageLabels(imageFile.Key));
        }
      });

      Promise.all(promises).then(results => {
        writeAnalysisResults(domain, results, createWordCloudList(results)).then(result => {
          resolve({statusCode: 200, body: JSON.stringify(result)});
        });
      });
    });
  });
}

// analyze images in bucket
function analyzeImages (event, context, cb) {
  'use strict';
  asyncMod.eachSeries(event.Records, (record, asyncCb) => {
    let { body } = record;

    try {
      body = JSON.parse(body);
    } catch (exp) {
      return asyncCb('message parse error: ' + record);
    }

    if (body.action === 'analyze' && body.msg && body.msg.domain) {
      iterateBucket(body.msg.domain, context).then(result => {
        asyncCb(null, result);
      });
    } else {
      asyncCb();
    }
  }, (err) => {
    if (err) { console.log(err); }
    cb();
  });
}

// entry point
module.exports = {
  analyzeImages
};
