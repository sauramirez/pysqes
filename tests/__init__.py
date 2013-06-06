from pysqes.task import SQSTask

import conf

task = SQSTask(
    aws_access_key=conf.AWS_ACCESS_KEY_ID,
    aws_secret_key=conf.AWS_SECRET_ACCESS_KEY)


@task.task
def add(a, b):
    """
    Create a task we can reuse in our tests
    """
    return a + b
