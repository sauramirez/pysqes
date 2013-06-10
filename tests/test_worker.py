from pysqes.worker import Worker

from tests import conn

worker = Worker(conn)
worker.work()
