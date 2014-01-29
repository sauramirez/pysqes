import unittest

from pysqes.queue import Queue
from pysqes.task import Task

from .stubs import SQSConnStub
from .test_tasks import add_func


class TestQueue(unittest.TestCase):

    def setUp(self):
        connection = SQSConnStub()
        self.queue = Queue(connection, 'pysqes_test')

    def test_enqueue_task(self):
        """
        Here we're actually testing both enqueue and dequeue methods
        from the queue.
        """

        task = Task(add_func, [1, 2])
        self.queue.enqueue_task(task)

        messages = self.queue.dequeue()
        self.assertEqual(messages[0][1]._args, [1, 2])

        task2 = Task(data={
            "key": 3
        })

        self.queue.enqueue_task(task2)
        messages2 = self.queue.dequeue()
        self.assertEqual(messages2[0][1].data, {"key": 3})

    def test_enqueue(self):
        self.queue.enqueue(add_func, 1, 2)

        messages = self.queue.dequeue()
        self.assertEqual(messages[0][1]._args, [1, 2])
