from pysqes.task import SQSTask

from tests.stubs import SQSConnStub


conn = SQSConnStub()
task = SQSTask(conn)


@task.task
def add(a, b):
    return a + b
