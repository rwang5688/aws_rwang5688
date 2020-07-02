async function hello(event) {
    'use strict';
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'Hello Serverless!',
            input: event
        },
        null, 2)
    };
}

module.exports = {
    hello
};
