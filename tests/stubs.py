import logging
import json
import time

from collections import deque


class SQSConnStub(object):

    def create_queue(self, name):
        return SQSQueueStub()

    def lookup(self, name):
        return SQSQueueStub()


class SQSQueueStub(object):
    _queue = deque()

    def write(self, m):
        return self._queue.append(m)

    def get_messages(self, *args, **kwargs):
        if len(self._queue):
            return [self._queue.popleft()]
        else:
            return []

    def delete_message(self, message):
        logging.info("deleting message %s" % message)

    def delete_message_batch(self, messages):
        logging.info("deleting messages %s" % messages)

    def read(self):
        return self._queue.popleft()


class SQSMessageStub(object):
    _id = None

    @property
    def id(self):
        if not self._id:
            self._id = time.clock() * 10000000
        return self._id

    def get_body(self):
        return json.dumps({
            'fun': '{0}.{1}'.format(add.__module__, add.__name__),
            'args': [1, 2],
            'kwargs': {}
        })


def add(x, y):
    """
    Simple function to be used as a task by the SQSMessageStub.
    """
    return x + y
