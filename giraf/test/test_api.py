from unittest import TestCase, main as ut_main

import giraf.api


class TestAPI(TestCase):

	def test_api(self):
		top_level_exports = ['Imgur', 'ImgurError', 'ImageType', 'ImageSize', 'QueryType', 'SortOption', 'WindowOption', 'GalleryType']
		giraf_api_dir = dir(giraf.api)

		for i in top_level_exports:
			self.assertIn(i, giraf_api_dir)


if __name__ == '__main__':
	ut_main()

