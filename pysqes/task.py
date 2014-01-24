"""
The Task module defines the basic delay tasks we can create.
"""
import json
import logging

from .utils import import_fn

logger = logging.getLogger(__name__)


class Task(object):
    _fn = None
    _args = None
    _kwargs = None
    _result = None
    backend = None

    # if we're not supposed to be serializing a function
    data = None

    @classmethod
    def unserialize_task(cls, blob, backend=None):
        """
        Create task object from an unserialized data string

        Args:
            blob (String) - String containing the task data. It can only handle json strings for now.

        Returns:
            task (Task) - Task instances with the data contained inside the blob
        """
        task_data = json.loads(blob)
        fn = task_data.get('_fn', None)
        json_data = None
        if fn:
            fn = import_fn(fn)
        else:
            json_data = task_data

        args = task_data.get('args', None)
        kwargs = task_data.get('kwargs', None)

        return cls(fn, args, kwargs, data=json_data, backend=backend)

    def __init__(self, fn=None, arguments=None, kw_args=None, *args, **kwargs):
        self._result = None
        if fn:
            self._fn_object = fn
            self._fn = "{0}.{1}".format(fn.__module__, fn.__name__)
            self._args = arguments if arguments else []
            self._kwargs = kw_args if kw_args else {}

        self.data = kwargs.pop('data', {})
        self.backend = kwargs.pop('backend', None)

    @property
    def func(self):
        if not self._fn:
            return None

        if not self._fn_object:
            return import_fn(self._fn)

        return self._fn_object

    def serialize(self):
        """
        Serialize the task data to a format that can be stored in the Queue

        Returns:
            (String) - serialized task data
        """
        # the data dictionary we'll be sending to the queue
        task_data = self.data
        if self._fn:
            task_data = {
                "_fn": self._fn,
                "args": self._args,
                "kwargs": self._kwargs
            }

        return json.dumps(task_data)

    def run(self):
        func = self.func
        if not func:
            raise Exception("No function associated with this task")

        success = False
        try:
            self._result = func(*self._args, **self._kwargs)
            success = True
        except Exception as e:
            self._result = e
        finally:
            # do any cleanup needed
            logger.debug("Result for task %s" % self._result)
            if self.backend:
                self.backend.store_result(success, self._result)

        return self._result
