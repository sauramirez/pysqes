

class SQSConnStub(object):

    def create_queue(self, name):
        return SQSQueueStub()


class SQSQueueStub(object):

    def write(self, m):
        return True
