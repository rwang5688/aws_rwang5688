const uuid = require('uuid');
const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = { TableName: process.env.TODO_TABLE };

// create HTTP response
function respond (err, body, cb) {
  'use strict';
  let statusCode = 200;

  body = body || {};
  if (err) {
    body.stat = 'err';
    body.err = err;
    if (err.statusCode) {
      statusCode = err.statusCode;
    } else {
      statusCode = 500;
    }
  } else {
    body.stat = 'ok';
  }

  const response = {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true,
      statusCode: statusCode
    },
    body: JSON.stringify(body)
  };

  cb(null, response);
}

// remove empty action and note
function removeEmpty (data) {
  'use strict';
  if (data.action.length === 0) { data.action = null; }
  if (data.note.length === 0) { data.note = null; }
}

// create
function create (event, context, cb) {
  'use strict';
  const data = JSON.parse(event.body);
  removeEmpty(data);

  data.id = uuid.v1();
  data.modifiedTime = new Date().getTime();

  const params = { ...TABLE_NAME, Item: data };
  dynamoDb.put(params, (err, data) => {
    respond(err, {data: data}, cb);
  });
}

// read
function read (event, context, cb) {
  'use strict';
  const params = { ...TABLE_NAME, Key: { id: event.pathParameters.id } };
  dynamoDb.get(params, (err, data) => {
    respond(err, data, cb);
  });
}

// update
function update (event, context, cb) {
  'use strict';
  const data = JSON.parse(event.body);
  removeEmpty(data);

  data.id = event.pathParameters.id;
  data.modifiedTime = new Date().getTime();
  const params = { ...TABLE_NAME, Item: data };

  dynamoDb.put(params, (err, data) => {
    console.log(err);
    console.log(data);
    respond(err, data, cb);
  });
}

// delete
function del (event, context, cb) {
  'use strict';
  const params = { ...TABLE_NAME, Key: { id: event.pathParameters.id } };
  dynamoDb.delete(params, (err, data) => {
    respond(err, data, cb);
  });
}

// list
function list (event, context, cb) {
  'use strict';
  const params = TABLE_NAME;
  dynamoDb.scan(params, (err, data) => {
    respond(err, data, cb);
  });
}

// entry points
module.exports = {
  create,
  read,
  update,
  del,
  list
};
