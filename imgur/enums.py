
from enum import Enum


ImageType 	= Enum('Imagetype', 	['jpg', 'png', 'gif', 'anigif', 'album'])
ImageSize 	= Enum('ImageSize', 	{'small': 'small', 'medium': 'med', 'big': 'big', 'large': 'lrg', 'huge': 'huge'})
QueryType 	= Enum('QueryType', 	{'all': 'q_all', 'any': 'q_any', 'exactly': 'q_exactly', 'not': 'q_not'})
SortOption 	= Enum('SortOptions', 	['time', 'viral', 'top'])
WindowOption 	= Enum('WindowOptions', ['week', 'month', 'year', 'all'])

names 		= lambda e : [m.name for m in e]
values 		= lambda e : [m.value for m in e]
enumattr	= lambda e, a : getattr(e, a, None) if a is not None else None

