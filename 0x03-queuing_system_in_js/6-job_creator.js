import kue from 'kue';

const queue = kue.createQueue({
  redis: {
    host: 'localhost',
    port: 6379,
  },
});

const jobData = {
  phoneNumber: "+2347024533540",
  message: "hey, there",
};

const notificationJob = queue.create('push_notification_code', jobData)
.save(err => {
  if (!err) {
    console.log('Notification job created:', notificationJob.id);
  } else {
    console.error('Error creating notification job:', err);
  }
});

notificationJob.on('complete', () => {
  console.log('Notification job completed');
})

notificationJob.on('failed', () => {
  console.log('Notification job failed');
});
