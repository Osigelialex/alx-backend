import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const subscribedChannel = "holberton school channel";

client.subscribe(subscribedChannel);
client.on('message', (channel, message) => {
  if (channel === subscribedChannel) {
    console.log(message);
    if (message === 'KILL_SERVER') {
      client.unsubscribe(subscribedChannel);
      client.quit();
    }
  }
});
