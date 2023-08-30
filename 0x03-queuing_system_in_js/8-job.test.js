import { expect } from 'chai';
import sinon from 'sinon';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('Push Notification Jobs', function () {
  let queue;

  beforeEach(function () {
    queue = kue.createQueue({ testMode: true });
  });

  afterEach(function (done) {
    queue.testMode.clear(done);
  });

  it('should create and enqueue push notification jobs', function () {
    const jobs = [
      {
        phoneNumber: '1234567890',
        message: 'Test message 1',
      },
      {
        phoneNumber: '9876543210',
        message: 'Test message 2',
      },
    ];

    createPushNotificationsJobs(queue, jobs);
    expect(queue.testMode.jobs.length).to.equal(jobs.length);

    jobs.forEach((jobData, index) => {
      const queuedJob = queue.testMode.jobs[index];
      expect(queuedJob.type).to.equal('push_notification_code_2');
      expect(queuedJob.data).to.deep.equal(jobData);
    });
  });

  it('should call the done callback when job completes', function (done) {
    const jobData = {
      phoneNumber: '1234567890',
      message: 'Test message',
    };

    const doneSpy = sinon.spy();

    createPushNotificationsJobs(queue, [jobData]);

    const job = queue.testMode.jobs[0];

    job.on('complete', doneSpy);

    job.emit('complete');

    expect(doneSpy.called).to.be.true;

    done();
  });

});

