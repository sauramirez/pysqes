


task = SQSTask(aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_key=AWS_SECRET_ACCESS_KEY)

@task.task
def add(a, b):
    return a + b
