

def get_image_link(gallery_image):
	if type(gallery_image) == dict:
		ga = lambda a : gallery_image.get(a, None)
	else:
		ga = lambda a : getattr(gallery_image, a, None)

	if not ga('animated'):
		return ga('link')
	else:
		return ga('webm')


def ifc(cond, a, b):
	if cond:
		return a
	else:
		return b

