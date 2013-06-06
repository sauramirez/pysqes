from pysqes.task import SQSTask

import conf

import pdb
pdb.set_trace()

task = SQSTask(
        aws_access_key=conf.AWS_ACCESS_KEY_ID,
        aws_secret_key=conf.AWS_SECRET_ACCESS_KEY)


@task.task
def add(a):
    pass
