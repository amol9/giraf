
from .enums import QueryType

class Filter:

	def __init__(self, pages=1, max_results=None, query=None, query_type=QueryType.all, gtype=None):
		self.pages 		= pages
		self.max_results	= max_results
		self.query		= query
		self.query_type		= query_type
		self.gtype		= gtype

	
	def match(self, result_item):
		pass
