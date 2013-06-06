

if __name__ == '__main__':
    worker = Worker(aws_access_key=AWS_ACCESS_KEY_ID, aws_secret_key=AWS_SECRET_ACCESS_KEY)
    worker.work()
