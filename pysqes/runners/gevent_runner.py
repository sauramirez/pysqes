from itertools import islice

import gevent

from . import BaseRunner


# python generator for this runner
def join_every(n, iterable):
    """
    This will run the gevent join all after n threads have been created
    """
    i = iter(iterable)
    iter_slice = list(islice(i, n))
    while iter_slice:
        yield iter_slice
        iter_slice = list(islice(i, n))


class GeventRunner(BaseRunner):
    current_threads = []

    def perform_tasks(self, tasks):
        gevent_threads = []
        running_tasks = []
        running_messages = []
        for gen_tasks in join_every(5, tasks):
            for message, task in gen_tasks:
                gevent_threads.append(gevent.spawn(task.run))
                running_tasks.append(task)
                running_messages.append(message)

            gevent.joinall(gevent_threads)
            self.finished_tasks(running_tasks, running_messages)

            running_tasks = []

    def perform_task(self, task):
        # wait for tasks to finish and rejoin them
        if len(self.current_threads) > 5:
            gevent.join_all(self.current_threads)
            self.current_threads = []

        self.current_threads.append(gevent.spawn(task.run))

    def shutdown(self):
        pass
