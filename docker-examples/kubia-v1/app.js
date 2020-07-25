const http = require('http');
const os = require('os');


function handler(request, response) {
  let clientIP = request.connection.remoteAddress;
  console.log("Received request for " + request.url + " from " + clientIP);
  response.writeHead(200);
  response.write("Hey there, this is " + os.hostname() + ". ");
  response.write("Your IP is " + clientIP + ". ");
  response.end("\n");
}

function main() {
  const listenPort = 8080;

  console.log("Kubia server starting...");
  console.log("Local hostname is " + os.hostname());
  console.log("Listening on port " + listenPort);

  let server = http.createServer(handler);
  server.listen(listenPort);
}

main();

