from unittest import TestCase, main as ut_main

import giraff.api


class TestAPI(TestCase):

	def test_api(self):
		top_level_exports = ['Imgur', 'ImgurError', 'ImageType', 'ImageSize', 'QueryType', 'SortOption', 'WindowOption', 'GalleryType']
		giraff_api_dir = dir(giraff.api)

		for i in top_level_exports:
			self.assertIn(i, giraff_api_dir)


if __name__ == '__main__':
	ut_main()

