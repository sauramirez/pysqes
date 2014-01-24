import errno
import signal
import time
import os
import multiprocessing
import logging

try:
    import gevent
    gevent_support = True
except ImportError:
    gevent_support = False

logger = logging.getLogger(__name__)


class Worker(object):
    """
    Workers are in charge of fetching new jobs from the queue and executing them
    if there are any.
    """
    _shutdown = False
    _child_process = 0
    # the backend should speciy a store_result method
    backend = None

    def __init__(self, queue, *args, **kwargs):
        """
        """
        self.queue = queue
        #self.backend = kwargs.pop('backend', None)

        # time to wait in between jobs
        self.wait_time = kwargs.pop('wait_time', 3)

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

        if self._child_process:
            try:
                os.kill(self._child_process, signal.SIGKILL)
            except OSError as e:
                # ESRCH ("No such process") is fine with us
                if e.errno != errno.ESRCH:
                    logger.debug('Process already down.')
                    raise

        raise SystemExit()

    def _shutdown_signal(self, signum, frame):
        self.shutdown()

    #new
    def run(self, task, thread=False):
        if not thread:
            self.register_signal_handlers()

        task.run()

    def work(self, thread=False):
        """
        This is the method in charge of fetching the jobs from SQS
        """
        if not thread:
            self.register_signal_handlers()

        # start running our worker
        while True:
            tasks = self.queue.dequeue()
            for message, task in tasks:
                result = self.perform_task(task)
                logger.info("Received result from task: {0}".format(result))
                self.queue.delete_message(message)

            if self._shutdown:
                break

    def perform_task(self, task):
        child_pid = os.fork()
        if child_pid == 0:
            result = task.run()
            print "Result %s" % result
            os._exit(int(not False))

        else:
            logger.info("Started forked worker")
            self._child_process = child_pid
            while True:
                try:
                    os.waitpid(child_pid, 0)
                    break
                except OSError as e:
                    if e.errno != errno.EINTR:
                        raise

            return True
