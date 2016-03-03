import sys
import webbrowser
from os import linesep
from os.path import exists
from base64 import b64decode

from redlib.api.misc import ob
from redlib.api.system import is_py3
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError 
from enum import Enum

from .pager import Pager
from .enums import QueryType, SortOption, WindowOption
from .filter import Filter
from .helper import get_image_link


__all__ = ['Imgur', 'ImgurError', 'ImgurErrorType'] 


ImgurErrorType = Enum('ImgurErrorType', ['not_found', 'capacity', 'other'])


class ImgurError(Exception):

	def __init__(self, msg, err_type=ImgurErrorType.other):
		super(ImgurError, self).__init__(msg)
		self.err_type = err_type


class Imgur:
	client_id = ob(b64decode('BwpTXAIFBlBNAwtFXFkP'))
	cred_file = '.cred'


	def __init__(self):
		if is_py3():
			self.client_id = self.client_id.decode('ascii')

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
		print(acct)


	def search(self, query, image_type=None, image_size=None, query_type=None, sort=SortOption.time, window=WindowOption.all,
			pages=1, max_results=None, gallery_type=None, animated=None):
		advanced = None

		if any(i is not None for i in [image_type, image_size, query_type]):
			advanced = {}
			if image_type is not None:
				advanced['q_type'] = image_type.name
			if image_size is not None:
				advanced['q_size_px'] = image_size.value
			if query_type is None:
				query_type = QueryType.all

			advanced[query_type.value] = query

		filter = Filter(gallery_type=gallery_type, animated=animated)
		pager = Pager(pages=pages, max_results=max_results, filter=filter)

		for page in pager.run(self.client.gallery_search, query, advanced=advanced, sort=sort.name, window=window.name):
			for r in page:
				yield r

	
	def album_info(self, album_id):
		return self.get_album(album_id)


	def get_album(self, album_id):
		try:
			album = self.client.get_album(album_id)
			return album
		except ImgurClientError as e:
			if e.status_code == 404:
				err_type = ImgurErrorType.not_found
			else:
				err_type = ImgurErrorType.other

			raise ImgurError(e, err_type=err_type)

	
	def album_image_urls(self, album_id):
		album = self.get_album(album_id)
		return [get_image_link(i) for i in album.images]

	
	def gallery_favorites(self, username, pages=1, max_results=None, query=None, query_type=None, gallery_type=None):
		filter = Filter(query=query, query_type=query_type, gallery_type=gallery_type)
		pager = Pager(pages=pages, max_results=max_results, filter=filter)

		for p in pager.run(self.client.get_gallery_favorites, username):
			yield p

