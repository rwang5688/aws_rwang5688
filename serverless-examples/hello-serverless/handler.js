async function helloServerless(event) {
  'use strict';
  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        message: 'helloServerless: Hello Serverless!',
        input: event
      },
      null,
      2)
    };
}

module.exports = {
  helloServerless
};
