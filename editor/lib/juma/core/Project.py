#!/usr/bin/env python
import logging
import sys
import imp
import os
import os.path
import re
import shutil
import hashlib
import time

import signals
import jsonHelper

# _GII_ENV_DIR            = 'env'
# _GII_GAME_DIR           = 'game'
# _GII_HOST_DIR           = 'host'
# _GII_BINARY_DIR         = 'bin'

# _GII_ASSET_DIR          = _GII_GAME_DIR + '/asset'
# _GII_SCRIPT_LIB_DIR     = _GII_GAME_DIR + '/lib'

# _GII_HOST_EXTENSION_DIR = _GII_HOST_DIR  + '/extension'

# _GII_ENV_PACKAGE_DIR    = _GII_ENV_DIR  + '/packages'
# _GII_ENV_DATA_DIR       = _GII_ENV_DIR  + '/data'
# _GII_ENV_LIB_DIR        = _GII_ENV_DIR  + '/lib'
# _GII_ENV_CONFIG_DIR     = _GII_ENV_DIR  + '/config'

_PROJECT_GAME_DIR			= 'lua'

_PROJECT_INFO_FILE          = 'project.json'
_PROJECT_CONFIG_FILE        = 'config.json'



##----------------------------------------------------------------##
def _affirmPath( path ):
	if os.path.exists( path ): return
	try:
		os.mkdir( path )
	except Exception, e:
		pass
		
##----------------------------------------------------------------##
class Project(object):
	_singleton=None
	@staticmethod
	def get():		
		return Project._singleton

	# @staticmethod
	# def findProject( path = None ):
	# 	#TODO: return project info dict instead of path?
	# 	path = os.path.abspath( path or '' )
	# 	opath = None
	# 	while path and not ( path in ( '', '/','\\' ) ):
	# 		if   os.path.exists( path + '/' + _GII_ENV_CONFIG_DIR ) \
	# 		and  os.path.exists( path + '/' + _GII_INFO_FILE ) :
	# 			#get info
	# 			info = jsonHelper.tryLoadJSON( path + '/' + _GII_INFO_FILE )
	# 			info['path'] = path
	# 			return info
	# 		#go up level
	# 		opath = path
	# 		path = os.path.dirname( path )
	# 		if path == opath: break
	# 	return None

	def __init__(self):
		assert not Project._singleton
		Project._singleton = self

		self.loaded 	= False
		self.path      	= None
		self.gamePath 	= None
		self.info 		= None

	def _initPath( self, path ):
		self.path = path

		self.gamePath          = path + '/' + _PROJECT_GAME_DIR

	def _affirmDirectories( self ):
		_affirmPath( self.gamePath )

	def init(self, path):
		signals.emitNow('project.init', self)

	def load(self, path):
		if not path:
			path = self.path
			if not self.path: return False

		if not os.path.exists( path + '/' + _PROJECT_INFO_FILE ): return False

		self._initPath( path )
		self._affirmDirectories()
		self.info = jsonHelper.tryLoadJSON( self.getBasePath( _PROJECT_INFO_FILE ) )

		self.loaded = True
		signals.emitNow( 'project.preload', self )
		signals.emitNow( 'project.load', self )

		return True

	def save(self):
		signals.emitNow('project.presave', self)
		#save project info & config
		jsonHelper.trySaveJSON( self.info, self.getBasePath( _PROJECT_INFO_FILE ), 'project info' )

		#save asset & cache
		# self.assetLibrary.save()
		# self.cacheManager.clearFreeCacheFiles()
		# self.cacheManager.save()

		signals.emitNow( 'project.save', self )
		return True

	def getPath( self, path = None ):
		return self.getBasePath( path )
		
	def getBasePath( self, path = None ):
		return os.path.join( self.path, path )

	def isLoaded( self ):
		return self.loaded

##----------------------------------------------------------------##

Project()
		