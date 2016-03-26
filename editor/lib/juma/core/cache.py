import os
import os.path
import logging
import hashlib
import shutil

import jsonHelper

##----------------------------------------------------------------##
class CacheManager(object):
	_singleton = None
	
	@staticmethod
	def get():
		return CacheManager._singleton

	def __init__( self ):
		assert not CacheManager._singleton
		CacheManager._singleton = self

		super(CacheManager, self).__init__()

	def save( self ):
		pass
		
	def clearFreeCacheFiles( self ):
		pass