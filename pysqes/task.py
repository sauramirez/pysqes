import time
import pickle

from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message

conn = None

SQS_TASKER = {
    'default': 'sqs-tasker'
}


def get_queue(queue='default', queues={}, aws_access_key=None, aws_secret_key=None):
    global conn

    if not aws_access_key:
        raise Exception("Need to provide an aws access key")
    if not aws_secret_key:
        raise Exception("Need to provide an aws secret key")

    if not conn:
        conn = SQSConnection(aws_access_key, aws_secret_key)
    queue = conn.create_queue(queues.get(queue))
    return queue


class DelayTask(object):
    task = None
    fun = None

    def __call__(self, *args, **kwargs):
        task_data = {
            'args': args,
            'kwargs': kwargs,
            'fun': self.fun
        }

        task_data = pickle.dumps(task_data)
        self.task.schedule_task(task_data)


class BasePySQS(object):

    def __init__(self, queue='default', backend=None, queues=None, aws_access_key=None, aws_secret_key=None):
        if not queues:
            queues = {
                'default': 'pysqes'
            }
        self.queue = get_queue(queue, queues=queues, aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)


class SQSTask(BasePySQS):
    callback = None

    def __init__(self, queue='default', backend=None, queues=None, aws_access_key=None, aws_secret_key=None):
        if not queues:
            queues = {
                'default': 'pysqes'
            }
        self.queue = get_queue(queue, queues=queues, aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)

    def task(self, fun):
        delay = DelayTask()
        delay.fun = fun
        delay.task = self
        setattr(fun, 'delay', delay)
        setattr(fun, '_task', self)

        return fun

    def schedule_task(self, data):
        queue = self.queue
        m = Message()
        m.set_body(data)
        status = queue.write(m)

        return status

    def run(self, task_data):
        if not self.callback:
            raise("Not implemented")

