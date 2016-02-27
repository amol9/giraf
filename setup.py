import ez_setup
ez_setup.use_setuptools()

import platform
import sys
from setuptools import setup, find_packages

from rc_setup import setup_autocomp

from imgur.version import __version__


entry_points = {}
entry_points['console_scripts'] = ['imgur=imgur.main:main']

setup(	
	name			= 'imgur',
	version			= __version__,
	description		= 'API and command line client for imgur.com.',
	author			= 'Amol Umrale',
	author_email 		= 'babaiscool@gmail.com',
	url			= 'http://pypi.python.org/pypi/imgur/',
	packages		= find_packages(), 
	include_package_data	= True,
	scripts			= ['ez_setup.py', 'rc_setup.py'],
	entry_points 		= entry_points,
	install_requires	= ['imgurpython>=1.1.7', 'redlib>=1.1.4', 'redcmd>=1.1.7', 'enum34'],
	classifiers		= [
					'Development Status :: 4 - Beta',
					'Environment :: Console',
					'License :: OSI Approved :: MIT License',
					'Natural Language :: English',
					'Operating System :: POSIX :: Linux',
					'Programming Language :: Python :: 2.7',
					'Programming Language :: Python :: 3.4'
				]
)


setup_autocomp('imgur.client.all_subcommands', 'imgur', _to_hyphen=True)

