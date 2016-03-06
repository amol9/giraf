

class Pager:

	def __init__(self, filter, method, param_name='page'):
		self._filter		= filter
		self._param_name 	= param_name
		self._method 		= method


	def run(self):
		start_page 	= self._filter.start_page
		pages 		= self._filter.pages
		max_results	= self._filter.max_results
		sort		= self._filter.sort
		window		= self._filter.window

		kwargs = {}

		if sort is not None:
			kwargs['sort'] = sort.name
		if window is not None:
			kwargs['window'] = window.name

		count = 0
		for page in range(start_page, start_page + pages):

			kwargs[self._param_name] = page
			result = self._method(**kwargs)

			if len(result) == 0:
				return

			fresult = []
			if self._filter is not None:
				for r in result:
					if self._filter.match(r):
						fresult.append(r)
			else:
				fresult = result

			if max_results is not None:
				d = max_results - count
				if d < len(fresult):
					del fresult[d : len(fresult)]

			for r in fresult:
				yield r

			count += len(fresult)

			if max_results is not None and count >= max_results:
				return

