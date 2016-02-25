
from enum import Enum
from imgurpython.helpers import GalleryAlbum, GalleryImage


__all__ = ['ImageType', 'ImageSize', 'QueryType', 'SortOption', 'WindowOption', 'GalleryType']


ImageType 	= Enum('Imagetype', 	['jpg', 'png', 'gif', 'anigif', 'album'])
ImageSize 	= Enum('ImageSize', 	{'small': 'small', 'medium': 'med', 'big': 'big', 'large': 'lrg', 'huge': 'huge'})
QueryType 	= Enum('QueryType', 	{'all': 'q_all', 'any': 'q_any', 'exactly': 'q_exactly', 'not': 'q_not'})
SortOption 	= Enum('SortOptions', 	['time', 'viral', 'top'])
WindowOption 	= Enum('WindowOptions', ['week', 'month', 'year', 'all'])
GalleryType	= Enum('GalleryType',	{'image': GalleryImage, 'album': GalleryAlbum})

