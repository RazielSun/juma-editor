import json
import re
import os
import logging
import os.path
import weakref

from abc import ABCMeta, abstractmethod

import jsonHelper
import signals

from cache import CacheManager

##----------------------------------------------------------------##
class AssetNode(object):
	def __init__(self, nodePath, assetType='file', **kwargs):
		self.nodePath   = nodePath
		self.assetType  = assetType
		self.name = os.path.basename( nodePath )

		self.children = []

	def __repr__(self):	
		return u'<{0}>{1}'.format( self.getType(), self.getNodePath() ).encode('utf-8')	

	def getName(self):
		return self.name

	def getType(self):
		return self.assetType

	def getNodePath( self ):
		return self.nodePath

	def getDir(self):
		return os.path.dirname( self.getNodePath() )

	def getChildren(self):
		return self.children

	def getChildrenCount(self):
		return len(self.children)

##----------------------------------------------------------------##
class AssetLibrary(object):
	"""docstring for AssetLibrary"""
	_singleton=None

	@staticmethod
	def get():
		return AssetLibrary._singleton

	def __init__(self):
		assert not AssetLibrary._singleton
		AssetLibrary._singleton=self

		self.assetTable      = {}
		self.assetIconMap    = {}

		# self.projectScanScheduled = False
		# self.cacheScanned    = False
		
		# self.assetManagers   = []
		# self.assetCreators   = []

		# self.rawAssetManager = RawAssetManager()
		
		# self.rootPath        = None

		# self.ignoreFilePattern = [
		# 	'\.git',
		# 	'\.assetmeta',
		# 	'^\..*',
		# 	'.*\.pyo$',
		# 	'.*\.pyc$'
		# ]

	# def load( self, rootPath, rootAbsPath, projectAbsPath, configPath ):
	# 	#load asset
	# 	self.rootPath       = rootPath
	# 	self.rootAbsPath    = rootAbsPath
	# 	self.projectAbsPath = projectAbsPath
	# 	self.assetIndexPath = configPath + '/' +GII_ASSET_INDEX_PATH
	# 	self.rootNode       = AssetRootNode( '', 'folder', filePath = self.rootPath )
	# 	# self.loadAssetTable()
	def save( self ):
		self.saveAssetTable()

	def saveAssetTable( self, **option ): #FIXME
		pass

	def loadAssetTable(self):
		pass

	def getAllAssets( self ):
		return self.assetTable.values()

	def getAssetTable( self ):
		return self.assetTable

	def hasAssetNode(self, nodePath):
		if not nodePath: return False
		return not self.getAssetNode( nodePath ) is None

	def getAssetNode(self, nodePath):
		if not nodePath: return self.rootNode
		return self.assetTable.get(nodePath, None)

	def getAssetIcon( self, assetType ):
		return self.assetIconMap.get( assetType, assetType )

	def setAssetIcon( self, assetType, iconName ):
		self.assetIconMap[ assetType ] = iconName

	def enumerateAsset( self, patterns, **options ):
		noVirtualNode = options.get( 'no_virtual', False )
		result = []
		subset = options.get( 'subset', self.assetTable.values() )
		
		if not patterns: # ALL
			for node in subset:
				if ( noVirtualNode and node.isVirtual() ) : continue
				result.append( node )
			return result

		if isinstance( patterns, ( str, unicode ) ): # match patterns
			patterns = patterns.split(';')
		matchPatterns = []
		for p in patterns:
			pattern = re.compile( p )
			matchPatterns.append( pattern )

		for node in subset:
			if ( noVirtualNode and node.isVirtual() ) : continue
			for matchPattern in matchPatterns:
				mo = matchPattern.match( node.getType() )
				if not mo: continue
				if mo.end() < len( node.getType() ) - 1 : continue
				result.append(node)
				break
		return result

	def registerAssetNode( self, node ):
		path = node.getNodePath()
		logging.info( 'register: %s' % repr(node) )
		if self.assetTable.has_key(path):
			raise Exception( 'unclean path: %s', path)
		self.assetTable[path]=node

		# signals.emit( 'asset.register', node )

		for child in node.getChildren():
			self.registerAssetNode(child)

		return node

	def clearAssets( self ):
		self.assetTable.clear()