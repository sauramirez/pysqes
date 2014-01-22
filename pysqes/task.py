"""
The Task module defines the basic delay tasks we can create.
"""
import json
import pickle
import uuid

from boto.sqs.message import Message

from .utils import import_fn

SQS_TASKER = {
    'default': 'sqs-tasker'
}


def get_queue(conn, queue='default', queues={}, aws_access_key=None, aws_secret_key=None):
    if not conn:
        raise ("Need to provide a valid AWS connection")

    sqs_queue = conn.lookup(queues.get(queue))
    if not sqs_queue:
        sqs_queue = conn.create_queue(queues.get(queue))

    return sqs_queue


class DelayTask(object):
    '''
    The default module to be used for serializing the data
    we receive, the serializer should implement the loads
    and dumps methods
    '''
    task = None
    fun = None

    def __call__(self, *args, **kwargs):
        task_data = {
            'args': args,
            'kwargs': kwargs,
            'fun': self.fun,
            'name': self.fun.__name__,
            'task_id': uuid.uuid4()
        }

        self.task.schedule_task(task_data)


class BasePySQS(object):
    serializer = pickle
    _queue = None

    def __init__(self, conn, queue='default',
                 queues=None, serializer=None):
        self.conn = conn
        if not queues:
            queues = {
                'default': 'pysqes'
            }

        self.queues = queues
        self.queue_name = queue
        if serializer:
            self.serializer = serializer

    @property
    def queue(self):
        if not self._queue:
            self._queue = get_queue(self.conn, self.queue_name, queues=self.queues)

        return self._queue


class Task(object):
    _fn = None
    _args = None
    _kwargs = None
    # if we're not supposed to be serializing a function
    data = None

    @classmethod
    def unserialize_task(cls, blob):
        """
        Create task object from an unserialized data string

        Args:
            blob (String) - String containing the task data. It can only handle json strings for now.

        Returns:
            task (Task) - Task instances with the data contained inside the blob
        """
        task_data = json.loads(blob)
        fn = task_data.get('_fn', None)
        fn = import_fn(fn)
        args = task_data.get('args', None)
        kwargs = task_data.get('kwargs', None)
        json_data = task_data.get('data', None)

        return cls(fn, args, kwargs, data=json_data)

    def __init__(self, fn=None, arguments=None, kw_args=None, *args, **kwargs):
        self._result = None
        if fn:
            self._fn_object = fn
            self._fn = "{0}.{1}".format(fn.__module__, fn.__name__)
            self._args = arguments if arguments else []
            self._kwargs = kw_args if kw_args else {}

        self.data = kwargs.pop('data', {})

    @property
    def func(self):
        if not self._fn:
            return None

        if not self._fn_object:
            return import_fn(self._fn)

        return self._fn_object

    def serialize(self):
        """
        Serialize the task data to a format that can be stored in the Queue

        Returns:
            (String) - serialized task data
        """
        # the data dictionary we'll be sending to the queue
        task_data = self.data
        if self._fn:
            task_data = {
                "_fn": self._fn,
                "args": self._args,
                "kwargs": self._kwargs
            }

        return json.dumps(task_data)

    def run(self):
        func = self.func
        try:
            self._result = func(*self._args, **self._kwargs)
        finally:
            # do any cleanup needed
            pass

        return self._result

    def task(self, fun):
        delay = DelayTask()
        delay.fun = fun
        delay.task = self
        setattr(fun, 'delay', delay)
        setattr(fun, '_task', self)

        return fun

    def schedule_task(self, data):
        queue = self.queue
        msg = Message()
        msg.set_body(self.serializer.dumps(data))
        status = queue.write(msg)

        return status
