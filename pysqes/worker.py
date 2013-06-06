import pickle
import time

from .task import BasePySQS


class Worker(BasePySQS):

    def work(self):
        while True:
            messages = self.queue.get_messages()
            for message in messages:
                task = message.get_body()
                task = pickle.loads(task)
                result = task['fun'](*task['args'], **task['kwargs'])
                print "result {0}".format(result)
                self.queue.delete_message(message)

                # should call a save function on the backend
            time.sleep(1)

    @classmethod
    def run(cls, queue, timeout):
        worker = cls(queue, timeout)
        worker.work()
