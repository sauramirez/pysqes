pysqes
======

Simple queue service for python using SQS and boto.

Usage
======
In order to create a task you can use the SQSTask class to create
an instance that include a function decorator which can be sent
to the queue when you run the delay method that will be added
to the function. The delay function takes the parameters that will
be used by the worker when it actually executes the task.

```python
from boto.sqs.connection import SQSConnection

from pysqes.task import SQSTask

conn = SQSConnection('ACCESS_KEY', 'SECRETE_KEY')
task = SQSTask(conn)


@task.task
def add(a, b):
    return a + b

# this will submit a job to the queue
add.delay(1, 3)
```

You can run the task by using the work method included in the
SQSWorker class, all you need to do is create a worker instance.
```python
from boto.sqs.connection import SQSConnection

from pysqes.worker import SQSWorker

conn = SQSConnection('ACCESS_KEY', 'SECRETE_KEY')
worker = SQSWorker(conn)

worker.work()
```

Running the tests
======
If you are using python 2.7 you can run the unit tests by
using the new discover runner included in the unittest module:

```shell
python -m unittest discover -s tests
```

else you can just run each unit test individually.

