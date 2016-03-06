
from redlib.api.py23 import enum_names, enum_values, enum_attr
from redcmd.api import Subcommand, subcmd, Arg, EnumArg

from ..enums import *
from ..imgur import Imgur
from ..filter import Filter

from .printers import ResultPrinter
from .subcommand_mixin import SubcommandMixin


class MainSubcommands(Subcommand, SubcommandMixin):

	#@subcmd
	def gallery(self):
		pass


	@subcmd(add=['result', 'sort', 'window', 'result_type'])
	def search(self, query, image_type=EnumArg(opt=True, choices=ImageType), image_size=EnumArg(opt=True, choices=ImageSize),
			query_type=EnumArg(opt=True, choices=QueryType)):

		'''Search imgur.
		query:		search term(s)
		image_type:	image type desired
		image_size:	image size desired
		query_type:	query type'''

		self._filter.query 	= query
		self._filter.image_type = image_type
		self._filter.image_size = image_size
		self._filter.query_type = query_type
		
		gen = self.exc_imgur_call(Imgur.search, self._filter)
		self.print_gen_result(gen)


	def print_gen_result(self, gen):
		printer = ResultPrinter(urls_only=self._urls_only)
		for r in gen:
			printer.printf(r)


	@subcmd(add=['result', 'opt_query'])
	def favorites(self, username):
		'''Get gallery favorites for a user.
		username:	username for the user'''

		gen = self.exc_imgur_call(Imgur.gallery_favorites, username, self._filter) 
		self.print_gen_result(gen)
	

	@subcmd(add=['result', 'opt_query'])
	def subreddit(self, subreddit):
		'''Get subreddit images.
		subreddit: 	subreddit name'''

		gen = self.exc_imgur_call(Imgur.subreddit, subreddit, self._filter)
		self.print_gen_result(gen)
