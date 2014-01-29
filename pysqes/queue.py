import logging

from boto.sqs.message import Message

from .task import Task

logger = logging.getLogger(__name__)


class Queue(object):
    _queue = None
    backend = None

    def __init__(self, connection, queue_name, queues=None, backend=None):
        """
        Args:
            connection (PysqesConnection) - Connection instance where we'll be sending
                messages to
            queue_name (String) - The way the queue is represented in SQS
        """
        self.connection = connection
        self.queue_name = queue_name
        self.queues = queues
        self.backend = backend

    @property
    def queue(self):
        if self._queue:
            return self._queue

        # if there is no queues dictionary we just use the queue_name attribute
        if not self.queues:
            queue_name = self.queue_name
        else:
            # if queues dictionary has been defined it should raise an exception
            # if the queue requested is not in it
            queue_name = self.queues[self.queue_name]

        queue = self.connection.lookup(queue_name)
        if not queue:
            logger.info("Creating new queue {0} in SQS".format(queue_name))
            queue = self.connection.create_queue(queue_name)

        self._queue = queue
        return queue

    def enqueue_task(self, task, delay_seconds=None):
        """
        Receives a task object that can be serialized and added to the queue
        so that a worker can pick it up later.
        """
        task_blob = task.serialize()
        msg = Message()
        msg.set_body(task_blob)
        status = self.queue.write(msg)

        return status

    def enqueue(self, fn, *args, **kwargs):
        """
        Delays the execution of fn until a worker picks it up
        """
        if fn.__module__ == '__main__':
            raise ValueError(
                "Can't send functions from the __main__ module.")

        task = Task(fn, args, kwargs)
        delay_seconds = kwargs.pop('delay_seconds', None)

        self.enqueue_task(task, delay_seconds=delay_seconds)

    def dequeue(self, num_messages=1, visibility_timeout=None, attributes=None, wait_time_seconds=None):
        """
        Get messages from the queue, the number of messages received depends on the num_messages argument

        Returns:
            (list) - List of messages received, it returns an empty list if no message is currently in the queue.
        """
        messages = self.queue.get_messages(num_messages, visibility_timeout=None, attributes=None, wait_time_seconds=None)

        tasks = []
        for message in messages:
            task_data = message.get_body()
            task = Task.unserialize_task(task_data, backend=self.backend)
            tasks.append((message, task))

        return tasks

    def delete_message(self, message):
        return self.queue.delete_message(message)

    def delete_message_batch(self, messages):
        return self.queue.delete_message_batch(messages)
