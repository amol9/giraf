
from redcmd.api import commandline_execute

from .client import Client
from . import const
from .version import __version__


def main():
	commandline_execute(	prog=const.program_name,
				description=const.program_desc,
				version=__version__,
				_to_hyphen=True)

