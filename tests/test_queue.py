import unittest

from pysqes.queue import Queue
from pysqes.task import Task

from .stubs import SQSConnStub, SQSQueueStub
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

    def test_get_queue(self):
        """Test getting queue name from dictionary"""
        connection = SQSConnStub()
        queue = Queue(connection, 'pysqes_test', {'pysqes_test': 'test'})
        queue_stub = queue.queue
        self.assertEqual(queue_stub.name, 'test')

    def test_not_queue_lookup(self):
        connection = SQSConnStub()
        queue = Queue(connection, False)
        queue_stub = queue.queue
        self.assertIsInstance(queue_stub, SQSQueueStub)

    def test_delete_messages(self):
        messages = self.queue.delete_message_batch(['message'])
        self.assertEqual(messages, ['message'])

    def test_delete_message(self):
        messages = self.queue.delete_message('message')
        self.assertEqual(messages, 'message')

    def test_enqueue_validation(self):
        def fn():
            pass
        fn.__module__ = '__main__'
        with self.assertRaises(ValueError):
            self.queue.enqueue(fn)
