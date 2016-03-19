import sys
import webbrowser
from os import linesep
from os.path import exists
from base64 import b64decode
import warnings
from functools import partial

from redlib.api.misc import ob
from redlib.api.system import is_py3
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError 
from enum import Enum
from requests.exceptions import SSLError

from .pager import Pager
from .enums import QueryType, SortOption, WindowOption, SubredditSortOption
from .filter import Filter
from .helper import get_image_link, ifc


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
			warnings.filterwarnings('ignore', category=ResourceWarning, module='.*imgurpython.*')

		self.client = self.exc_call(ImgurClient, self.client_id, '')

	
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


	def search(self, filter):
		default_filter = Filter(sort=SortOption.time, window=WindowOption.all)
		filter.add(default_filter)

		advanced = None

		if any(i is not None for i in [filter.image_type, filter.image_size, filter.query_type]):
			advanced = {}
			if filter.image_type is not None:
				advanced['q_type'] = filter.image_type.name
			if filter.image_size is not None:
				advanced['q_size_px'] = filter.image_size.value
			if filter.query_type is None:
				filter.query_type = QueryType.all

			advanced[filter.query_type.value] = filter.query

		method = partial(self.client.gallery_search, filter.query, advanced=advanced)
		pager = Pager(filter, method)
		return self.exc_call(pager.run)

	
	def album_info(self, album_id):
		return self.get_album(album_id)


	def get_album(self, album_id):
		return self.exc_call(self.client.get_album, album_id)


	def exc_call(self, method, *args, **kwargs):
		try:
			return method(*args, **kwargs)

		except ImgurClientError as e:
			err_type = ifc(e.status_code == 404, ImgurErrorType.not_found, ImgurErrorType.other)
			raise ImgurError(e, err_type=err_type)

		except SSLError as e:
			raise ImgurError(str(e))

	
	def album_image_urls(self, album_id):
		album = self.get_album(album_id)
		return [get_image_link(i) for i in album.images]

	
	def gallery_favorites(self, username, filter):
		method = partial(self.client.get_gallery_favorites, username) 
		pager = Pager(filter, method)
		return self.exc_call(pager.run)


	def subreddit(self, sub, filter):
		default_filter = Filter(sort=SubredditSortOption.time, window=WindowOption.week)
		filter.add(default_filter)

		method = partial(self.client.subreddit_gallery, sub)
		pager = Pager(filter, method)
		return self.exc_call(pager.run)


	def get_image(self, image_id):
		return self.exc_call(self.client.get_image, image_id)

