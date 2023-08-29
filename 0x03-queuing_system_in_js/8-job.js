import kue from 'kue';

const queue = kue.createQueue({
  redis: {
    host: 'localhost',
    port: 6379,
  },
});

export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  for (const job of jobs) {
    const notificationJob = queue.create('push_notification_code_3')
    .save(err => {
      if (!err) {
        console.log(`Notification job created: ${notificationJob.id}`);
      }
    });

    notificationJob.on('completed', () => {
      console.log(`Notification job ${notificationJob.id} completed`);
    })

    notificationJob.on('failed', (err) => {
      console.log(`Notification job ${notificationJob.id} failed: ${error}`);
    });

    notificationJob.on('progress', (progress) => {
      console.log(`Notification job ${notificatitonJob.id} ${progress}% complete`);
    })
  } 
}
