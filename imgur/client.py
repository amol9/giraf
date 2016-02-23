
from redcmd.api import Subcommand, subcmd, Arg, CommandError
from .cls_imgur import Imgur, ImgurError


class Client(Subcommand):

	def __init__(self):
		self._imgur = None


	def exc_imgur_call(self, meth, *args, **kwargs):
		try:
			if self._imgur is None:
				self._imgur = Imgur()

			meth(self._imgur, *args, **kwargs)
		except ImgurError as e:
			print(e)
			raise CommandError()


	@subcmd
	def gallery(self):
		pass

	@subcmd
	def search(self, query, 
			image_type=Arg(opt=True, default=None, choices=Imgur.image_types),
			image_size=Arg(opt=True, default=None, choices=Imgur.image_sizes.keys()),
			query_type=Arg(opt=True, default=None, choices=Imgur.query_types.keys()),
			sort=Arg(opt=True, default='time', choices=Imgur.sort_options),
			window=Arg(opt=True, default='all', choices=Imgur.window_options),
			pages=1, max_results=None):

		'''Search imgur.
		query:		search term(s)
		image_type:	image type desired
		image_size:	image size desired
		query_type:	query type
		sort:		sort options
		window:		date range for results
		pages:		number of pages of results needed'''

		try:
			pages = int(pages)
			if pages < 0:
				print('number of pages should be >0')
				raise CommandError()
			max_results = int(max_results) if max_results is not None else None
		except ValueError as e:
			print(e)
			raise CommandError()

		self.exc_imgur_call(Imgur.search, query, image_type, image_size, query_type, sort, window, pages, max_results=max_results)


	@subcmd
	def album(self):
		pass


