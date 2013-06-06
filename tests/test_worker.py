import conf

from pysqes.worker import Worker

worker = Worker(
    aws_access_key=conf.AWS_ACCESS_KEY_ID,
    aws_secret_key=conf.AWS_SECRET_ACCESS_KEY)
worker.work()
