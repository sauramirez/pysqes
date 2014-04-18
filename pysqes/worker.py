import signal
import logging

from time import sleep

from .runners.process_runner import ProcessRunner

logger = logging.getLogger(__name__)


class Worker(object):
    """
    Workers are in charge of fetching new jobs from the queue and executing them
    if there are any.
    """
    _shutdown = False
    # the backend should speciy a store_result method
    backend = None
    runner = None
    # number of messages to get from the queue at the same time
    num_messages = 5
    delay = 1

    def __init__(self, queue, runner=None, num_messages=5, *args, **kwargs):
        """
        """
        self.queue = queue

        # time to wait in between jobs
        self.wait_time = kwargs.pop('wait_time', 3)
        self.num_messages = num_messages
        self.delay = kwargs.pop('delay', 1)

        if runner:
            self.runner = runner
        else:
            self.runner = ProcessRunner()

        # set the runner worker delegate
        self.runner.worker = self

    def register_signal_handlers(self):
        """
        Register our handlers so that we can stop the process from running
        """
        signal.signal(signal.SIGTERM, self._shutdown_signal)
        signal.signal(signal.SIGINT, self._shutdown_signal)
        signal.signal(signal.SIGQUIT, self._shutdown_signal)
        signal.signal(signal.SIGUSR1, self._shutdown_signal)

    def shutdown(self):
        self._shutdown = True
        self.runner.shutdown()

        raise SystemExit()

    def _shutdown_signal(self, signum, frame):
        self.shutdown()

    def work(self, thread=False):
        """
        This is the method in charge of fetching the jobs from SQS
        """
        if not thread:
            self.register_signal_handlers()

        # start running our worker
        while True:
            tasks = self.queue.dequeue(num_messages=self.num_messages)
            if tasks:
                self.runner.perform_tasks(tasks)
            else:
                # no tasks wait for a small time before checking again
                sleep(self.delay)

            if self._shutdown:
                break

    def finished_task(self, message):
        return self.queue.delete_message(message)

    def finished_tasks(self, messages):
        return self.queue.delete_message_batch(messages)
