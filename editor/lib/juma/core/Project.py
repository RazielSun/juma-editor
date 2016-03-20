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

	def __init__(self):
		assert not Project._singleton
		Project._singleton = self

		self.path      	= None
		self.gamePath 	= None

		self.info 		= None
		self.config 	= None

	def _initPath( self, path ):
		self.path = path

		self.gamePath          = path + '/' + _PROJECT_GAME_DIR

	def _affirmDirectories( self ):
		_affirmPath( self.gamePath )

	def isLoaded( self ):
		return self.path != None

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
		self.config = jsonHelper.tryLoadJSON( self.getBasePath( _PROJECT_CONFIG_FILE ) )
		if not self.config:
			self.config = {}
			self.saveConfig()

		self.loaded = True
		signals.emitNow( 'project.preload', self )
		signals.emitNow( 'project.load', self )

		return True

	def save(self):
		signals.emitNow('project.presave', self)
		jsonHelper.trySaveJSON( self.info, self.getBasePath( _PROJECT_INFO_FILE ) )
		signals.emitNow( 'project.save', self )
		return True

	def saveConfig( self ):
		jsonHelper.trySaveJSON( self.config, self.getConfigPath( _PROJECT_CONFIG_FILE ))

	def getPath( self, path = None ):
		return self.getBasePath( path )
		
	def getBasePath( self, path = None ):
		return os.path.join( self.path, path )

	def getConfigPath(self, path=None):
		return os.path.join( self.path, path )

##----------------------------------------------------------------##
	def getConfigDict( self ):
		return self.config

	def getConfig( self, key, default = None ):
		if self.config:
			return self.config.get( key, default )
		return default

	def setConfig( self, key, value ):
		self.config[ key ] = value

##----------------------------------------------------------------##

Project()
		