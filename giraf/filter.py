
from .enums import QueryType, GalleryType


__all__ = ['Filter']


class FilterResult:
	def __init__(self):
		self.clear()


	def clear(self):
		self.failed 	= 0
		self.matched	= 0
		self.total	= 0


class Filter:

	def __init__(self, pages=1, max_results=None, query=None, query_type=None, gallery_type=None, animated=None,
			min_size=None, start_page=0, sort=None, window=None, image_size=None, image_type=None, max_filesize=None):

		self.pages 		= pages
		self.max_results	= max_results
		self.query		= query.lower() if query is not None else None
		self.query_type		= query_type if query_type is not None else QueryType.all
		self.gallery_type	= gallery_type
		self.animated		= animated
		self.min_size		= min_size
		self.start_page		= start_page
		self.sort		= sort
		self.window		= window
		self.image_size		= image_size
		self.image_type		= image_type
		self.max_filesize	= max_filesize

		self.result		= FilterResult()

	
	def match(self, result_item):
		result = True
		self.result.total += 1

		if self.gallery_type is not None and type(result_item) != self.gallery_type.value:
			return False

		if type(result_item) == GalleryType.image.value:
			if self.animated is not None and result_item.animated != self.animated:
				return False
			if self.max_filesize is not None and result_item.size > self.max_filesize:
				return False
			if self.min_size is not None and (result_item.width < self.min_size[0] or result_item.height < self.min_size[1]):
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

	
	def add(self, filter):
		assert filter.__class__ == Filter

		if filter is None:
			return

		attr_list = ['pages', 'max_results', 'query', 'query_type', 'gallery_type', 'animated', 'min_size', 'start_page',
				'sort', 'window', 'image_size']

		for attr in attr_list:
			if getattr(self, attr, None) is None:
				setattr(self, attr, getattr(filter, attr, None))

