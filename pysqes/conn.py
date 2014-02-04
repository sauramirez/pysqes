from boto.sqs.connection import SQSConnection


class Connection():
    """
    This class acts as a facade for an SQSConnection
    so that we connect to SQS it until we need it.

    See http://docs.pythonboto.org/en/latest/ref/sqs.html#module-boto.sqs.connection for
    a list of all the methods you can use.
    """
    conn = None
    aws_access_key = None
    aws_secret_key = None

    def __init__(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def __getattr__(self, name, *args, **kwargs):
        '''
        A method is being called that can be passed on to
        the SQSConnection object.
        '''
        if not self.conn and self.aws_access_key and self.aws_secret_key:
            self.conn = SQSConnection(self.aws_access_key, self.aws_secret_key)

        return getattr(self.conn, name)

    def __repr__(self):
        return 'Connection'
