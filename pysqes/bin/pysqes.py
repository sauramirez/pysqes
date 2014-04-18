import sys
import logging

from ..conn import Connection
from ..utils import import_module

from .base import BaseCommand
from .worker import WorkerCommand

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main(argv=None):
    pysqes_command = PysqesCommand()
    pysqes_command.run_from_commandline(argv)


class HelpCommand(BaseCommand):
    pass


class PysqesCommand(BaseCommand):
    commands = {
        'worker': WorkerCommand,
        'help': HelpCommand
    }

    def get_subcommand_cls(self, subcommand):
        logger.info("Getting subcommand {0}".format(subcommand))
        command_cls = self.commands.get(subcommand) or self.commands['help']
        return command_cls

    def run_from_argv(self, argv):
        if len(argv) < 2:
            logger.debug("You need to specify a command")
            raise Exception("Not enough arguments, missing pysqes command")

        command_cls = self.get_subcommand_cls(argv[1])
        command = command_cls()
        logger.debug(command)
        parser = command.get_parser(argv[0], argv[1])
        options, arguments = self.prepare_arguments(*parser.parse_args(argv[2:]))
        self.execute(command, arguments, options)

    def prepare_arguments(self, options, arguments):
        """
        Map options inside a dicitionary so that we can use it
        as keyword arguments.
        """
        if options:
            options = dict(
                (k, v)
                for k, v in vars(options).iteritems()
            )

        return options, arguments

    def execute(self, command, arguments, options):
        """
        The execute command takes the options provided and create an sqs connection
        instance that will be passed to the actual command. This allows
        the command to only focus on the tasks that they have to handle.
        """
        arguments, kwarguments = self.config_pysqes(arguments, options)
        kwarguments['connection'] = Connection(
            options.get('aws_access_key'),
            options.get('aws_secret_access_key')
        )

        command.handle(*arguments, **kwarguments)

    def config_pysqes(self, arguments, options):
        """
        Args:
            options (dict) - The parsed arguments provided from the command line.
        """
        aws_access_key = options['aws_access_key_id']
        aws_secret_access_key = options['aws_secret_access_key']

        if aws_access_key and aws_secret_access_key:
            return

        try:
            if not options.get('config', None):
                raise Exception("AWS keys weren't provided. Either use the \
                    aws options or provide a the path to a config file.")

            config_module = options.get('config')
            config_path = options.get('configpath')
            if config_path:
                sys.path.append(config_path)
                logger.info("Appended {0} to the sys path: {1}".format(config_path, sys.path))

            pysqesconfig = import_module(config_module)
            options['settings'] = pysqesconfig

            if not aws_access_key:
                aws_access_key = getattr(pysqesconfig, 'AWS_ACCESS_KEY', None)
                options['aws_access_key'] = aws_access_key

            if not aws_secret_access_key:
                aws_secret_access_key = getattr(pysqesconfig, 'AWS_SECRET_ACCESS_KEY', None)
                options['aws_secret_access_key'] = aws_secret_access_key

        except ImportError:
            pass

        if not aws_access_key or aws_secret_access_key is None:
            raise Exception("AWS keys are needed for the worker")

        return arguments, options

    def handle(self, *args, **kwargs):
        pass


if __name__ == '__main__':          # pragma: no cover
    main()
