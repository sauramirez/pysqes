from boto.sqs.connection import SQSConnection


class PysqesConnection():
    """
    This class acts as a lazy loader for an SQSConnection
    so that we connect to SQS it until we need it.
    """
    conn = None

    def __init__(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def __getattr__(self, name, *args, **kwargs):
        '''
        A method is being called that can be passed on to
        the SQSConnection object.
        '''
        if not self.conn:
            self.conn = SQSConnection(self.aws_access_key, self.aws_secret_key)

        return getattr(self.conn, name)

    def __repr__(self):
        return 'PysqesConnection'
