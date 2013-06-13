from boto.sqs.connection import SQSConnection

from pysqes.task import SQSTask

conn = SQSConnection('ACCESS_KEY', 'SECRETE_KEY')
task = SQSTask(conn)


@task.task
def add(a, b):
    return a + b

# this will submit a job to the queue
add.delay(1, 3)

import json
# you can also pick a different serializer
json_task = SQSTask(conn, serializer=json0

json_task.schedule_task({
    'test': 'json serializer'
})
