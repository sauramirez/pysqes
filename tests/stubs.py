import pickle


class SQSConnStub(object):

    def create_queue(self, name):
        return SQSQueueStub()


class SQSQueueStub(object):

    def write(self, m):
        return True

    def get_messages(self):
        return [SQSMessageStub()]

    def delete_message(self, message):
        pass


class SQSMessageStub(object):
    def get_body(self):
        return pickle.dumps({
            'fun': add,
            'args': [1, 2],
            'kwargs': {}
        })


def add(x, y):
    """
    Simple function to be used as a task by the SQSMessageStub.
    """
    return x + y
