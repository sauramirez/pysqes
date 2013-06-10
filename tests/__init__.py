from boto.sqs.connection import SQSConnection

from pysqes.task import SQSTask

import conf

conn = SQSConnection(conf.AWS_ACCESS_KEY_ID, conf.AWS_SECRET_ACCESS_KEY)
task = SQSTask(conn)


@task.task
def add(a, b):
    """
    Create a task we can reuse in our tests
    """
    return a + b
