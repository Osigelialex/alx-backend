import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server')
});

const pairs = { 
  "Portland": 50,
  "Seattle": 80,
  "New York": 20,
  "Bogota": 20,
  "Cali": 40,
  "Paris": 2
}

const data = Object.entries(pairs);
let key, value;

for ([key, value] of data) {
  client.hset('HolbertonSchools', key, value, (err, reply) => {
    if (err) {
      console.log(err);
    } else {
      console.log(`Reply: ${reply}`);
    }
  })
}

client.hgetall('HolbertonSchools', (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(data);
  }
})
