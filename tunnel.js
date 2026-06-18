const localtunnel = require('localtunnel');

(async () => {
  const tunnel = await localtunnel({ port: 8000 });
  console.log("BACKEND_URL=" + tunnel.url);
  console.log("API_URL=" + tunnel.url + "/api/v1");
  
  tunnel.on('close', () => {
    console.log('Tunnel closed');
  });
})();