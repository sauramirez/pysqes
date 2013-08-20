import threading
import unittest

from pysqes.worker import SQSWorker

from tests.stubs import SQSConnStub


class WorkerBackend(object):
    last_result = None

    def store_result(self, result):
        self.last_result = result


class WorkerThread(threading.Thread):
    worker = None

    def run(self):
        self.worker.work(thread=True)


class TestPysqesWorker(unittest.TestCase):

    def setUp(self):
        conn = SQSConnStub()
        self.worker = SQSWorker(conn)
        self.worker.backend = WorkerBackend()
        self.backend = self.worker.backend

    def test_work(self):
        workThread = WorkerThread()
        workThread.worker = self.worker
        workThread.start()

        # wait for a result to be stored
        while not self.backend.last_result:
            pass

        self.worker.shutdown()
        self.assertEquals(self.backend.last_result, 3)


if __name__ == '__main__':
    unittest.main()