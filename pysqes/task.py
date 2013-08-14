"""
The Task module defines the basic delay tasks we can create.
"""
import pickle

from boto.sqs.message import Message

SQS_TASKER = {
    'default': 'sqs-tasker'
}


def get_queue(conn, queue='default', queues={}, aws_access_key=None, aws_secret_key=None):
    if not conn:
        raise ("Need to provide a valid AWS connection")
    queue = conn.create_queue(queues.get(queue))
    return queue


class DelayTask(object):
    task = None
    fun = None
    # the default module to be used for serializing the data
    # we receive, the serializer should implement the loads
    # and dumps methods

    def __call__(self, *args, **kwargs):
        task_data = {
            'args': args,
            'kwargs': kwargs,
            'fun': self.fun
        }

        self.task.schedule_task(task_data)


class BasePySQS(object):
    serializer = pickle

    def __init__(self, conn, queue='default', backend=None,
                 queues=None, serializer=None):
        if not queues:
            queues = {
                'default': 'pysqes'
            }
        self.queue = get_queue(conn, queue, queues=queues)
        if serializer:
            self.serializer = serializer


class SQSTask(BasePySQS):
    callback = None

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
        m.set_body(self.serializer.dumps(data))
        status = queue.write(m)

        return status

    def run(self, task_data):
        if not self.callback:
            raise("Not implemented")
