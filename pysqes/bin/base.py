import logging
import sys

from optparse import make_option, OptionParser

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class BaseCommand(object):
    option_list = (
        make_option(
            '-v', '--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2', '3'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output'
        ),
        make_option(
            '--aws_access_key_id', action='store', dest='aws_access_key_id', default=None,
            help='The aws access key id so that we can retrieve jobs from sqs'
        ),
        make_option(
            '--aws_secret_access_key', action='store', dest='aws_secret_access_key',
            default=None,
            help='The aws secret access key so that we can retrieve jobs from sqs'
        ),
        make_option(
            '--queue', action='store', dest='queue', default='pysqes',
            help="The name of the SQS queue. The default is pysqes."
        ),
        make_option(
            '--config', action='store', dest='config', default=None,
            help="The path to the pysqes config module."
        ),
        make_option(
            '--configpath', action='store', dest='configpath', default=None,
            help="The directory path to the pysqes config module. If your config module is not in the PYTHONPATH, then set this option so that it can be appended to sys.path"
        )
    )
    prog_name = "pysqes"
    help = ""
    args = ""

    def usage(self, subcommand):
        usage = '%prog {0} [options] {1}'.format(subcommand, self.args)
        if self.help:
            return '{0}\n\n{1}'.format(usage, self.help)
        else:
            return usage

    def run_from_argv(self, argv):
        if len(argv) < 2:
            logger.debug("You need to specify a command")
            raise Exception("Not enough arguments, missing pysqes command")

        self.execute(argv[0], argv[1])

    def run_from_commandline(self, argv):
        argv = sys.argv if argv is None else argv
        logger.info("Running with arguments {0}".format(argv))
        return self.run_from_argv(argv)

    def get_parser(self, prog_name, subcommand):
        return OptionParser(
            prog=prog_name,
            usage=self.usage(subcommand),
            option_list=self.option_list
        )

    def handle(self):
        raise NotImplementedError('Command subclasses should implement this method')
