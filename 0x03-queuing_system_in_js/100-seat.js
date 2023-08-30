import kue from 'kue';
import redis from 'redis';
import express from 'express';
import { promisify } from 'util';

const queue = kue.createQueue({
  redis: {
    host: 'localhost',
    port: 6379
  }
});

const app = express();
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const reservationEnabled = true;
const PORT = 1245;

const reserveSeat = (number) => {
  client.set("available_seats", number.toString());
}

reserveSeat(50);

const getCurrentAvailableSeats = async () => {
  const availableSeats = await getAsync("available_seats");
  return availableSeats;
}

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  const data = { "numberofAvailableSeats": availableSeats };
  res.send(JSON.stringify(data));
});

app.get('/reserve_seat', async(req, res) => {
  const reservationJob = queue.create('reserve_seat')
  .save( err => {
    if (!err) {
      const data = { "status": "Reservation in process" };
      res.send(JSON.stringify(data));
      return;
    } else {
      const data = { "status": "Reservation failed" };
      res.send(JSON.stringify(data));
      return;
    }
  });

  reservationJob.on("complete", () => {
    console.log(`Seat reservation job ${reservationJob.id} completed`);
  });

  reservationJob.on("failed", (err) => {
    console.log(`Seat reservation job ${reservationJob.id} failed: ${err}`);
  });

  if (!reservationEnabled) {
    const data = { "status": "Reservations are blocked" };
    res.send(JSON.stringify(data));
    return;
  }
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    reserveSeat(availableSeats - 1);

    if (availableSeats === 0) reservationEnabled = false;
    if (availableSeats >= 0) {
      done();
    } else {
      done(new Error("Not enough seats available"));
    }
  })
  res.send(JSON.stringify({ "Status": "Queue processing" }));
});

app.listen(PORT);
