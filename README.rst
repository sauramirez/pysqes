pysqes
======

*Simple queue service for python using SQS and boto.*

.. image:: https://travis-ci.org/sauramirez/pysqes.png
   :alt: Build Status
   :target: https://travis-ci.org/sauramirez/pysqes


Usage
======
In order to create a task you can use the SQSTask class to create
an instance that include a function decorator which can be sent
to the queue when you run the delay method that will be added
to the function. The delay function takes the parameters that will
be used by the worker when it actually executes the task.

.. code-block:: python

    from boto.sqs.connection import SQSConnection
    from pysqes.task import Task

    conn = SQSConnection('ACCESS_KEY', 'SECRET_KEY')
    queue = Queue(conn, 'pysqes_test', backend=backend)

    def add(a, b):
        return a + b

    # this will submit a job to the queue
    queue.enqueue(add, 1, 2)

You can run the task by using the work method included in the
SQSWorker class, all you need to do is create a worker instance.

.. code-block:: python

    from boto.sqs.connection import SQSConnection
    from pysqes.runners.gevent_runner import GeventRunner
    from pysqes.worker import Worker

    conn = SQSConnection('ACCESS_KEY', 'SECRETE_KEY')
    runner = GeventRunner()
    queue = Queue(conn, 'pysqes_test', backend=backend)
    worker = Worker(queue, runner=runner)

    worker.work()

New in 0.2
======

Worker Runners
=====
Pysqes now supports having different runners, the default one is the
process runner, which will spawn a new a process and run the task in it.
We also have a gevent runner, which you can use by using the gevent flag
in the command line and set the number of threads you would like to have
running. 
Note: It has only been tested with gevent 1.0

Command line scripts
=====
Pysqes now comes with command line scripts. The worker command will be the only
one available for this version, but task and peek commands may be coming to 0.3.

.. code-block:: bash

    pysqes worker --gevent --workerpath=/home/user/pysqesproj/ --config=pysqesconfig --configpath=/home/user/pysqesproj/settings/

Running the tests
======
If you are using python 2.7 you can run the unit tests by
using the new discover runner included in the unittest module:

.. code-block:: bash

    python -m unittest discover -s tests

or you can just run each unit test individually.


Coming in 0.3
======
* New command line scripts.
* Tests for command line scripts.
* Better logging.
