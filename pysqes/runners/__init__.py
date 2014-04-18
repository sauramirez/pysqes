import logging

logger = logging.getLogger(__name__)


class BaseRunner(object):
    _worker = None

    @property
    def worker(self):
        if not self._worker:
            logger.debug("Worker hasn't been set")

        return self._worker

    @worker.setter
    def worker(self, worker):
        self._worker = worker

    def perform_tasks(self, tasks):
        """
        Perform the array of tasks sent to us.
        """
        raise NotImplemented()

    def perform_task(self, task, message):
        """
        Perform the task received and return a result for it.
        """
        raise NotImplemented()

    def finished_task(self, message):
        self.worker.finished_task(message)

    def finished_tasks(self, messages):
        self.worker.finished_tasks(messages)
