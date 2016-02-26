
from redcmd.api import Subcommand, subcmd, Arg, CommandError

from ..cls_imgur import Imgur

from .subcommand_mixin import SubcommandMixin
from .printers import AlbumInfoPrinter


class AlbumSubcommands(Subcommand, SubcommandMixin):

	@subcmd
	def album(self):
		'Commands to get album info / image url list, etc.'
		pass


class AlbumSubSubcommands(AlbumSubcommands):

	def album_id_common(self, album_id):
		'album_id:	id of the imgur album'

		self._album_id = album_id


	@subcmd(add=[album_id_common])
	def info(self):
		'Get album information.'

		album = self.exc_imgur_call(Imgur.album_info, self._album_id)
		printer = AlbumInfoPrinter()
		printer.printf(album)


	@subcmd(add=[album_id_common])
	def urls(self):
		'Dump image urls from album.'

		urls = self.exc_imgur_call(Imgur.album_image_urls, self._album_id)
		for u in urls:
			print(u)

