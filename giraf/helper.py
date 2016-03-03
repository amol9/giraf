

def get_image_link(gi):
	if not gi.animated:
		#return gi.get('link', None)
		return gi.link
	else:
		return gi.webm
		#return gi.get('webm', None)

