
from redcmd.api import CommandError, IntArg, EnumArg

from ..enums import *
from ..imgur import Imgur, ImgurError
from ..filter import Filter


class SubcommandMixin(object):

	def __init__(self):
		self._imgur = None
		self._filter = Filter()


	def exc_imgur_call(self, meth, *args, **kwargs):
		try:
			if self._imgur is None:
				self._imgur = Imgur()

			return meth(self._imgur, *args, **kwargs)
		except ImgurError as e:
			print(e)
			raise CommandError()


	def result(self, pages=IntArg(opt=True, default=1, max=500, min=1), max_results=IntArg(opt=True, max=10000, min=1),
			urls_only=False):
		'''Common params for subcommands that return results.
		pages:		number of pages of results needed
		max_results:	maximum number of results needed
		urls_only:	output only urls'''

		self._filter.pages 		= pages
		self._filter.max_results 	= max_results
		self._urls_only = urls_only


	def opt_query(self, query=None, query_type=EnumArg(opt=True, default=QueryType.all, choices=QueryType)):
		'''query:		query to filter the results
		query_type:		query type'''

		self._filter.query = query
		self._filter.query_type = query_type


	def window(self, window=EnumArg(opt=True, default=WindowOption.all, choices=WindowOption)):
		'window:		date range for results'
		self._filter.window = window


	def sort(self, sort=EnumArg(opt=True, default=SortOption.time, choices=SortOption)):
		'sort:		sort options'
		self._filter.sort = sort


	def result_type(self, result_type=EnumArg(opt=True, choices=GalleryType)):
		'result_type:	album / image'
		self._filter.gallery_type = result_type
	

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


