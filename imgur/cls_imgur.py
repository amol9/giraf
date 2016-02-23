import sys
import webbrowser
from os import linesep
from os.path import exists

from redlib.api.prnt import *
from imgurpython import ImgurClient


class Imgur:
	
	client_id = '3210fb6c4dc60b8'
	cred_file = '.cred'


	def __init__(self):
		self.client = ImgurClient(self.client_id, '') #self.client_secret)

	
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


	def search(self, query):
		result = self.client.gallery_search('ignored', advanced={'q_type': 'jpg', 'q_size_px': 'med', 'q_all': query})
		for r in result:
			if getattr(r, 'width', None) is not None:
				prints('%dx%d'%(r.width, r.height))
			if getattr(r, 'type', None) is not None:
				prints(' ' + r.type)

			print()


	def album(self, aid):
		a = self.client.get_album(aid)
		print a.title, a.images_count

