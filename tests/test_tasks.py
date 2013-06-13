import unittest
import json

from pysqes.task import SQSTask

from tests.task_stub import add
from tests.stubs import SQSConnStub


class TestPysqesTask(unittest.TestCase):
    def setUp(self):
        conn = SQSConnStub()
        self.conn = conn
        self.task = SQSTask(conn)

    def test_schedule_task(self):
        status = self.task.schedule_task({})
        self.assertTrue(status, msg="Error scheduling task")

    def test_delay(self):
        """
        Test that the decorator is actually working and delaying a task
        """
        add.delay(1, 2)
        self.assertIsNotNone(add.delay)

    def test_serializer(self):
        task = SQSTask(self.conn, serializer=json)
        status = task.schedule_task({})
        self.assertTrue(status, msg="Error with the serializer")


if __name__ == '__main__':
    unittest.main()
