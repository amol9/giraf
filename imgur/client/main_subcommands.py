
from redlib.api.py23 import enum_names, enum_values, enum_attr
from redcmd.api import Subcommand, subcmd, Arg

from ..enums import *
from ..cls_imgur import Imgur

from .printers import ResultPrinter
from .subcommand_mixin import SubcommandMixin


class MainSubcommands(Subcommand, SubcommandMixin):

	#def __init__(self):
	#	super(MainSubcommands, self).__init__()


	@subcmd
	def gallery(self):
		pass


	@subcmd(add=[SubcommandMixin.result_common])
	def search(self, query, 
			image_type=Arg(opt=True, default=None, choices=enum_names(ImageType)),
			image_size=Arg(opt=True, default=None, choices=enum_names(ImageSize)),
			query_type=Arg(opt=True, default=None, choices=enum_names(QueryType)),
			sort=Arg(opt=True, default=enum_names(SortOption)[0], choices=enum_names(SortOption)),
			window=Arg(opt=True, default=enum_names(WindowOption)[0], choices=enum_names(WindowOption))):

		'''Search imgur.
		query:		search term(s)
		image_type:	image type desired
		image_size:	image size desired
		query_type:	query type
		sort:		sort options
		window:		date range for results'''

		gen = self.exc_imgur_call(Imgur.search, query, 
				enum_attr(ImageType, image_type), enum_attr(ImageSize, image_size), enum_attr(QueryType, query_type),
				sort, window, self._pages, max_results=self._max_results)
		self.print_gen_result(gen)


	def print_gen_result(self, gen):
		printer = ResultPrinter()
		for r in gen:
			printer.printf(r)


	@subcmd(add=[SubcommandMixin.result_common])
	def favorites(self, username, query=None, query_type=None):
		'''Get gallery favorites for a user.
		username:	username for the user
		result_type:	album / image
		query:		query to filter the results
		query_type:	query type'''

		gen = self.exc_imgur_call(Imgur.gallery_favorites, username, pages=self._pages, max_results=self._max_results)
		self.print_gen_result(gen)
	
