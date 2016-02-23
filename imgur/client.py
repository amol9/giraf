
from redcmd.api import Subcommand, subcmd, Arg, CommandError
from .cls_imgur import Imgur


class Client(Subcommand):

	@subcmd
	def gallery(self):
		pass

	@subcmd
	def search(self):
		pass

	@subcmd
	def album(self):
		pass


