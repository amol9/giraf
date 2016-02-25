
from redlib.api.py23 import enum_names, enum_values, enum_attr

from redcmd.api import Subcommand, subcmd, Arg, CommandError
from .cls_imgur import Imgur, ImgurError
from .result_printer import ResultPrinter
from .enums import *


class Client(Subcommand):

	def __init__(self):
		self._imgur = None


	def exc_imgur_call(self, meth, *args, **kwargs):
		try:
			if self._imgur is None:
				self._imgur = Imgur()

			return meth(self._imgur, *args, **kwargs)
		except ImgurError as e:
			print(e)
			raise CommandError()


	@subcmd
	def gallery(self):
		pass


	def result_common(self, pages=1, max_results=None):
		'''Common params for subcommands that return results.
		pages:		number of pages of results needed
		max_results:	maximum number of results needed'''

		self._pages = self.validate_int(pages, min=0, desc='number of pages')
		self._max_results = self.validate_int(max_results, min=0, desc='number of results')


	@subcmd(add=[result_common])
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


	@subcmd
	def album(self, album_id):
		self.exc_imgur_call(Imgur.album, album_id)


	@subcmd(add=[result_common])
	def favorites(self, username, query=None, query_type=None):
		'''Get gallery favorites for a user.
		username:	username for the user
		result_type:	album / image
		query:		query to filter the results
		query_type:	query type'''

		gen = self.exc_imgur_call(Imgur.gallery_favorites, username, pages=self._pages, max_results=self._max_results)
		self.print_gen_result(gen)


	def validate_int(self, val, min=None, max=None, desc='value'):
		res = None
		if val is not None:
			try:
				res = int(float(val))
				if min is not None and res < min:
					print('%s should be >%d'%(desc, min))
					raise CommandError()
			except ValueError as e:
				print("math says '%s' is not a valid number"%val)
				raise CommandError()

		return res


