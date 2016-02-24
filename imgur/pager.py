

class Pager:

	def __init__(self, pages=1, max_results=None, param_name='page'):
		self._pages 		= pages
		self._max_results 	= max_results
		self._param_name 	= param_name


	def run(self, meth, *args, **kwargs):
		count = 0
		for page in range(0, self._pages):
			kwargs[self._param_name] = page
			result = meth(*args, **kwargs)

			if len(result) == 0:
				return

			if self._max_results is not None:
				d = self._max_results - count
				if d < len(result):
					del result[d : len(result)]

			yield result
			count += len(result)

			if self._max_results is not None and count >= self._max_results:
				return

