
from redlib.api.prnt import ColumnPrinter
from ..enums import GalleryType


class ResultPrinter:
	up_arrow = u'\u2b06'
	down_arrow = u'\u2b07'


	def __init__(self):
		self._start_count = 1


	def printf(self, result):
		#iprinter = ColumnPrinter(cols=[8, 10, -1])
		#aprinter = ColumnPrinter(cols=[8, 12, -1])

		for r in result:
			print(u'{0:03d}. {1}'.format(self._start_count, r.title))

			if type(r) == GalleryType.image.value:
				width = getattr(r, 'width', 0)
				height = getattr(r, 'height', 0)
				dimensions = '%dx%d'%(width, height)
				score = u'%s %d %s %d'%(self.up_arrow, r.ups, self.down_arrow, r.downs)
				print(u'  {0:<8} {1:<10} {2:<14} {3}'.format('Image', dimensions, score, r.link))
				#iprinter.printf('Image', dimensions, score, r.link)
			else:
				print('  {0:<8} {1:<12} {2}'.format('Album', str(r.images_count) + ' images', r.link))
				#aprinter.printf('Album', str(r.images_count) + ' images', r.link)
			
			self._start_count += 1


class AlbumInfoPrinter:
	fields = [('title', 'Title'), ('description', 'Description'), ('images_count', 'Images'), ('views', 'Views'), ('account_url', 'Account')]

	def __init__(self):
		pass

	def printf(self, album):
		printer = ColumnPrinter(cols=[15, -1])

		for field, title in self.fields:
			printer.printf(title + ':', str(getattr(album, field, '')))

