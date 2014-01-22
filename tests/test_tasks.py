import unittest
import json

from pysqes.task import Task
from pysqes.queue import Queue

#from tests.task_stub import add
#from tests.stubs import SQSConnStub


#class TestPysqesTask(unittest.TestCase):
    #def setUp(self):
        #conn = SQSConnStub()
        #self.conn = conn
        #self.task = SQSTask(conn)

    #def test_schedule_task(self):
        #status = self.task.schedule_task({})
        #self.assertTrue(status, msg="Error scheduling task")

    #def test_delay(self):
        #"""
        #Test that the decorator is actually working and delaying a task
        #"""
        #add.delay(1, 2)
        #self.assertIsNotNone(add.delay)

    #def test_serializer(self):
        #task = SQSTask(self.conn, serializer=json)
        #status = task.schedule_task({})
        #self.assertTrue(status, msg="Error with the serializer")


def test_func(a, b, *args, **kwargs):
    return a + b


class TestTask(unittest.TestCase):
    def setUp(self):
        pass

    def test_serialize(self):
        task = Task(test_func, [1, 2])
        task_data = task.serialize()
        print task_data
        self.assertEqual(task_data, '{"args": [1, 2], "_fn": "tests.test_tasks.test_func", "kwargs": {}}', msg="Error in task serialization")

    def test_run(self):
        task = Task(test_func, [1, 2])

        result = task.run()
        self.assertEqual(result, 3, msg="Result is not correct for the arguments provided")

    def test_unserialize_task(self):
        task = Task(test_func, [1, 2])
        task_data = task.serialize()

        task2 = Task.unserialize_task(task_data)
        self.assertEqual(task._fn, task2._fn)
        self.assertEqual(task._args, task2._args)
        self.assertEqual(task._kwargs, task2._kwargs)


if __name__ == '__main__':
    unittest.main()
