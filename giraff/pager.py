

class Pager:

	def __init__(self, pages=1, max_results=None, param_name='page', filter=None):
		self._pages 		= pages
		self._max_results 	= max_results
		self._param_name 	= param_name
		self._filter		= filter


	def run(self, meth, *args, **kwargs):
		count = 0
		for page in range(0, self._pages):
			kwargs[self._param_name] = page
			result = meth(*args, **kwargs)

			if len(result) == 0:
				return

			fresult = []
			if self._filter is not None:
				for r in result:
					if self._filter.match(r):
						fresult.append(r)
			else:
				fresult = result

			if self._max_results is not None:
				d = self._max_results - count
				if d < len(fresult):
					del fresult[d : len(fresult)]

			yield fresult
			count += len(fresult)

			if self._max_results is not None and count >= self._max_results:
				return

