import sys
from optparse import make_option

from boto.sqs.connection import SQSConnection

from ..runners.gevent_runner import GeventRunner
from ..worker import Worker
from ..queue import Queue

from .base import BaseCommand


class WorkerCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--gevent',
            action="store_true",
            dest='gevented',
            default=False,
            help="Use the gevent runner to execute tasks"
        ),
        make_option(
            '--workerpath',
            action="store",
            dest='worker_path',
            default=None,
            help="Path to be appended so that the worker can import the function being executed."
        ),
    )

    def handle(self, gevented=False, worker_path=None, *args, **kwargs):

        queue = Queue(kwargs.get('connection'), kwargs.get('queue'))
        settings = kwargs.get('settings', None)
        backend = None
        if settings:
            backend = getattr(settings, 'BACKEND', None)

        if worker_path:
            sys.path.append(worker_path)

        runner = None
        if gevented:
            runner = GeventRunner()

        worker = Worker(queue, runner=runner, backend=backend)
        worker.work()
