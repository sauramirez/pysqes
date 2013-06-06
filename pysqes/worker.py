import pickle
import signal
import time

from .task import BasePySQS


class Worker(BasePySQS):
    _shutdown = False

    def register_signal_handlers(self):
        """
        Register our handlers so that we can stop the process from runing
        """
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGQUIT, self.shutdown)
        signal.signal(signal.SIGUSR1, self.shutdown)

    def shutdown(self, signum, frame):
        self._shutdown = True

    def work(self):
        self.register_signal_handlers()

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

            if self._shutdown:
                break

    @classmethod
    def run(cls, queue, timeout):
        worker = cls(queue, timeout)
        worker.work()
