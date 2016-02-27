
from redcmd.api import CommandError

from ..imgur import Imgur, ImgurError


class SubcommandMixin(object):

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


	def result_common(self, pages=1, max_results=None):
		'''Common params for subcommands that return results.
		pages:		number of pages of results needed
		max_results:	maximum number of results needed'''

		self._pages = self.validate_int(pages, min=0, desc='number of pages')
		self._max_results = self.validate_int(max_results, min=0, desc='number of results')


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


