import logging
import threading
import unittest
import time
import tempfile

from pysqes.worker import Worker
from pysqes.queue import Queue
from pysqes.runners.gevent_runner import GeventRunner

from tests.stubs import SQSConnStub

from .test_tasks import test_func

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class WorkerBackend(object):
    """
    Simple backend that stores the result in last_result so that we can
    test that the workers are storing the result if a backend is present.
    """
    last_result = None
    file_name = None

    def __init__(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.file_name = f.name
        f.close()

    def store_result(self, success, result, *args, **kwargs):
        self.last_result = result

        with open(self.file_name, 'w+b') as f:
            f.write(str(result))

    @property
    def result(self):
        """
        Retrieve the result from somewhere
        """
        with open(self.file_name, 'r') as f:
            last_result = f.read()

        return last_result


class WorkerThread(threading.Thread):
    worker = None

    def run(self):
        self.worker.work(thread=True)


class TestPysqesWorker(unittest.TestCase):

    def setUp(self):
        connection = SQSConnStub()
        self.backend = WorkerBackend()
        self.queue = Queue(connection, 'pysqes_test', backend=self.backend)

    def test_worker(self):
        self.queue.enqueue(test_func, 1, 2)

        runner = GeventRunner()
        worker = Worker(self.queue, runner=runner)
        runner.worker = worker
        workThread = WorkerThread()
        workThread.worker = worker
        workThread.start()
        try:
            time.sleep(1)
            worker.shutdown()
        except:
            pass

        logger.info("Verifying result {0}".format(self.backend.result))
        self.assertEqual(self.backend.result, '3')

    def test_worker_process(self):
        self.queue.enqueue(test_func, 1, 2)

        worker = Worker(self.queue)
        workThread = WorkerThread()
        workThread.worker = worker
        workThread.start()
        try:
            time.sleep(1)
            worker.shutdown()
        except:
            pass

        logger.info("Verifying result {0}".format(self.backend.result))
        self.assertEqual(self.backend.result, '3')


if __name__ == '__main__':
    unittest.main()
