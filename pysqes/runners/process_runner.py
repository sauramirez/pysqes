import errno
import logging
import os
import signal

from . import BaseRunner

logger = logging.getLogger(__name__)


class ProcessRunner(BaseRunner):
    """
    Simple process runner. This will create a new process that will
    run the task in the background.
    """
    _child_process = 0

    def perform_tasks(self, tasks):
        messages = []
        for message, task in tasks:
            self.perform_task(task, False)
            messages.append(message)

        self.finished_tasks(messages)

    def perform_task(self, task, delete_message=True):
        child_pid = os.fork()
        if child_pid == 0:
            try:
                result = task.run()
            except Exception, e:
                result = e

            logger.info("Result %s" % result)
            if delete_message:
                self.finished_task(task[0])

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

    def shutdown(self):
        if self._child_process:
            try:
                os.kill(self._child_process, signal.SIGKILL)
            except OSError as e:
                # ESRCH ("No such process") is fine with us
                if e.errno != errno.ESRCH:
                    logger.debug('Process already down.')
                    raise
