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

    def finished_task(self, task):
        self.worker.finished_task(task)

    def finished_tasks(self, tasks, messages):
        self.worker.finished_tasks(tasks, messages)
