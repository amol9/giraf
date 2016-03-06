import sys

from redlib.api.prnt import ColumnPrinter
from redlib.api.system import is_py3

from ..enums import GalleryType
from ..helper import get_image_link


enc_utf8 = sys.stdout.encoding == 'UTF-8'


def ignore_u(s):
	if enc_utf8:
		return s

	if is_py3():
		s2 = bytes(s, 'utf-8') if type(s) == str else s
		return s2.decode('ascii', 'ignore')
	else:
		return s.decode('unicode_escape').encode('ascii', 'ignore')


def str_if_not(s):
	#print('s: ' + s + str(type(s)))
	if is_py3():
		if not (type(s) == str or type(s) == bytes):
			return str(s)
	else:
		if not (type(s) == str or type(s) == unicode):
			return str(s)
	return s


class ResultPrinter:
	up_arrow = u'\u2b06' if enc_utf8 else 'u'
	down_arrow = u'\u2b07' if enc_utf8 else 'd'


	def __init__(self, urls_only=False):
		self._start_count = 1
		self._urls_only = urls_only

		#iprinter = ColumnPrinter(cols=[8, 10, -1])
		#aprinter = ColumnPrinter(cols=[8, 12, -1])


	def printf(self, r):
		if self._urls_only:
			self.printf_urls_only(r)
			return

		print(u'{0:03d}. {1}'.format(self._start_count, ignore_u(r.title)))

		if type(r) == GalleryType.image.value:
			width = getattr(r, 'width', 0)
			height = getattr(r, 'height', 0)
			dimensions = '%dx%d'%(width, height)

			if r.ups is not None and r.downs is not None:
				score = u'%s %d %s %d'%(self.up_arrow, r.ups, self.down_arrow, r.downs)
			else:
				score = ''
			print(u'     {0:<8} {1:<10} {2:<14} {3}'.format('Image', dimensions, score, get_image_link(r)))
			#iprinter.printf('Image', dimensions, score, r.link)
		else:
			print('     {0:<8} {1:<12} {2}'.format('Album', str(r.images_count) + ' images', r.link))
			#aprinter.printf('Album', str(r.images_count) + ' images', r.link)
		
		self._start_count += 1


	def printf_urls_only(self, r):
		if type(r) == GalleryType.image.value:
			print(get_image_link(r))
		else:
			print(r.link)


class AlbumInfoPrinter:
	fields = [('title', 'Title'), ('description', 'Description'), ('images_count', 'Images'), ('views', 'Views'), ('account_url', 'Account')]

	def __init__(self):
		pass

	def printf(self, album):
		printer = ColumnPrinter(cols=[15, -1])

		for field, title in self.fields:
			printer.printf(title + ':', ignore_u(str_if_not(getattr(album, field, ''))))

