
from redlib.api.py23 import enum_names, enum_values, enum_attr
from redcmd.api import Subcommand, subcmd, Arg

from ..enums import *
from ..imgur import Imgur

from .printers import ResultPrinter
from .subcommand_mixin import SubcommandMixin


class MainSubcommands(Subcommand, SubcommandMixin):

	#def __init__(self):
	#	super(MainSubcommands, self).__init__()


	#@subcmd
	def gallery(self):
		pass


	@subcmd(add=[SubcommandMixin.result_common])
	def search(self, query, 
			image_type=Arg(opt=True, default=None, choices=enum_names(ImageType)),
			image_size=Arg(opt=True, default=None, choices=enum_names(ImageSize)),
			query_type=Arg(opt=True, default=None, choices=enum_names(QueryType)),
			sort=Arg(opt=True, default=SortOption.time.name, choices=enum_names(SortOption)),
			window=Arg(opt=True, default=WindowOption.all.name, choices=enum_names(WindowOption)),
			result_type=Arg(opt=True, default=None, choices=enum_names(GalleryType))):

		'''Search imgur.
		query:		search term(s)
		image_type:	image type desired
		image_size:	image size desired
		query_type:	query type
		sort:		sort options
		window:		date range for results
		result_type:	album / image'''

		gen = self.exc_imgur_call(Imgur.search, query, 
				image_type=enum_attr(ImageType, image_type), image_size=enum_attr(ImageSize, image_size),
				query_type=enum_attr(QueryType, query_type), sort=sort, window=window, pages=self._pages,
				max_results=self._max_results, gallery_type=enum_attr(GalleryType, result_type))

		self.print_gen_result(gen)


	def print_gen_result(self, gen):
		printer = ResultPrinter()
		for r in gen:
			printer.printf(r)


	@subcmd(add=[SubcommandMixin.result_common])
	def favorites(self, username, query=None,
			query_type=Arg(opt=True, default=None, choices=enum_names(QueryType)),
			result_type=Arg(opt=True, default=None, choices=enum_names(GalleryType))):

		'''Get gallery favorites for a user.
		username:	username for the user
		query:		query to filter the results
		query_type:	query type
		result_type:	album / image'''

		gen = self.exc_imgur_call(Imgur.gallery_favorites, username, pages=self._pages, max_results=self._max_results,
				query=query, query_type=enum_attr(QueryType, query_type), gallery_type=enum_attr(GalleryType,result_type))

		self.print_gen_result(gen)
	
