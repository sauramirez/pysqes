import unittest

from pysqes.task import Task

from .utils import add_func


class TestTask(unittest.TestCase):
    def setUp(self):
        pass

    def test_serialize(self):
        task = Task(add_func, [1, 2])
        task_data = task.serialize()

        self.assertEqual(task_data, '{"args": [1, 2], "_fn": "tests.utils.add_func", "kwargs": {}}', msg="Error in task serialization")

        task2 = Task(data={
            "key": 3
        })

        task2_data = task2.serialize()
        self.assertEqual(task2_data, '{"key": 3}', msg="Data couldn't be serialized")

    def test_run(self):
        task = Task(add_func, [1, 2])

        result = task.run()
        self.assertEqual(result, 3, msg="Result is not correct for the arguments provided")

        task2 = Task(data={
            "key": 3
        })

        with self.assertRaises(Exception):
            task2.run()

    def test_unserialize_task(self):
        task = Task(add_func, [1, 2])
        task_data = task.serialize()

        task2 = Task.unserialize_task(task_data)
        self.assertEqual(task._fn, task2._fn)
        self.assertEqual(task._args, task2._args)
        self.assertEqual(task._kwargs, task2._kwargs)


if __name__ == '__main__':
    unittest.main()
