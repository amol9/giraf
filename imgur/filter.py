
from .enums import QueryType, GalleryType

class Filter:

	def __init__(self, pages=1, max_results=None, query=None, query_type=None, gallery_type=None):
		self.pages 		= pages
		self.max_results	= max_results
		self.query		= query.lower() if query is not None else None
		self.query_type		= query_type if query_type is not None else QueryType.all
		self.gallery_type	= gallery_type

	
	def match(self, result_item):
		result = True

		if self.gallery_type is not None and type(result_item) != self.gallery_type.value:
			return False

		if self.query is not None:
			title = result_item.title.lower()

			if self.query_type == QueryType.exactly:
				return title.find(self.query) > -1
			else:
				query_terms = self.query.split()
				match_func = None

				if self.query_type == QueryType.all:
					match_func = all
				elif self.query_type == QueryType.any:
					match_func = any
				elif self.query_type == QueryType['not']:
					match_func = lambda x : not any(x)

				return match_func([title.find(t) > -1 for t in query_terms])

		return result

