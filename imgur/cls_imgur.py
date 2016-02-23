import sys
import webbrowser
from os import linesep
from os.path import exists

from redlib.api.prnt import *
from imgurpython import ImgurClient
from imgurpython.helpers import GalleryAlbum, GalleryImage


class ImgurError(Exception):
	pass


class Imgur:
	
	client_id = '3210fb6c4dc60b8'
	cred_file = '.cred'

	image_types = ['jpg', 'png', 'gif', 'anigif', 'album']
	image_sizes = {'small': 'small', 'medium': 'med', 'big': 'big', 'large': 'lrg', 'huge': 'huge'}
	query_types = {'all': 'q_all', 'any': 'q_any', 'exactly': 'q_exactly', 'not': 'q_not'}

	sort_options = ['time', 'viral', 'top']
	window_options = ['week', 'month', 'year', 'all']


	def __init__(self):
		self.client = ImgurClient(self.client_id, '')

	
	def auth(self):
		if exists(self.cred_file):
			at, rt = self.load_cred()
			self.client.set_user_auth(at, rt)
		else:
			self.authorize()


	def authorize(self):
		authorization_url = self.client.get_auth_url('pin')
		print('opening browser tab for authorization..')
		webbrowser.open_new_tab(authorization_url)

		pin = raw_input('enter pin: ')

		credentials = self.client.authorize(pin.strip(), 'pin')

		self.client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

		self.store_cred(credentials['access_token'], credentials['refresh_token'])


	def store_cred(self, at, rt):
		with open(self.cred_file, 'w') as f:
			f.write(at + linesep)
			f.write(rt + linesep)


	def load_cred(self):
		at = rt = None

		with open(self.cred_file, 'r') as f:
			lines = f.read().splitlines()
			at = lines[0]
			rt = lines[1]

		return at, rt


	def get_account(self):
		acct = self.client.get_account('')
		import pdb; pdb.set_trace()
		print(acct)


	def search(self, query, image_type, image_size, query_type, sort, window, pages, max_results=None):
		advanced = None

		if any(i is not None for i in [image_type, image_size, query_type]):
			advanced = {}
			if image_type is not None:
				advanced['q_type'] = image_type
			if image_size is not None:
				advanced['q_size_px'] = self.image_sizes[image_size]
			if query_type is not None:
				advanced[self.query_types[query_type]] = query

		result_start = 1
		for page in range(0, pages):
			result = self.client.gallery_search(query, advanced=advanced, sort=sort, window=window, page=page)
			if max_results is not None:
				d = max_results - result_start + 1
				if d < len(result):
					del result[d : len(result)]

			self.print_result(result, result_start)
			result_start += len(result)


	def print_result(self, result, start_count):
		count = start_count
		up_arrow = u'\u2b06'
		down_arrow = u'\u2b07'

		for r in result:
			print(u'{0:03d}. {1}'.format(count, r.title))

			if type(r) == GalleryImage:
				width = getattr(r, 'width', 0)
				height = getattr(r, 'height', 0)
				dimensions = '%dx%d'%(width, height)
				score = u'%s %d %s %d'%(up_arrow, r.ups, down_arrow, r.downs)
				print(u'  {0:<8} {1:<10} {2:<14} {3}'.format('Image', dimensions, score, r.link))
			else:
				print('  {0:<8} {1:<12} {2}'.format('Album', str(r.images_count) + ' images', r.link))
			count += 1


	def album(self, aid):
		a = self.client.get_album(aid)
		print a.title, a.images_count

