import logging
import json
import weakref
import base64
import moaipy

from exceptions import *
from juma.core  import *
from moaipy 	import *

##----------------------------------------------------------------##
def getDict( d, key, default=None ):
	return d.get( key, default )

def setDict( d, key, value ):
	d[key] = value

def decodeDict(data):
	return json.loads(data)

def encodeDict(dict):
	return json.dumps(dict).encode('utf-8')

##----------------------------------------------------------------##
## ModelBridge
##----------------------------------------------------------------##
class LuaObjectModelProvider(ModelProvider):
	def __init__( self,  name, priority, getTypeId, getModel, getModelFromTypeId ):
		self.name        = name
		self.priority    = priority

		self._getTypeId          = getTypeId
		self._getModel           = getModel
		self._getModelFromTypeId = getModelFromTypeId

	def getPriority( self ):
		return self.priority

	def getTypeId( self, obj ):
		if isinstance( obj, moaipy._LuaObject ):
			return self._getTypeId( obj )
		else:
			return None

	def getModel( self, obj ):
		if isinstance( obj, moaipy._LuaObject ):
			return self._getModel( obj )
		else:
			return None

	def getModelFromTypeId( self, typeId ):
		return self._getModelFromTypeId( typeId )

##----------------------------------------------------------------##
class LuaObjectAttr( Attr ):
	pass

##----------------------------------------------------------------##
class LuaObjectModel(ObjectModel):
	def __init__( self, name ):
		self.name = name

##----------------------------------------------------------------##
class ModelBridge(object):
	_singleton=None

	@staticmethod
	def get():
		return ModelBridge._singleton

	def __init__(self):
		assert(not ModelBridge._singleton)
		ModelBridge._singleton = self
		self.modelProviders   = []
		# SIGNALS
		signals.connect( 'moai.clean', self.cleanLuaBridgeReference )

	def newLuaObjectModel(self, name):
		return LuaObjectModel("LuaObjectModel_{}".format(name))

	def buildLuaObjectModelProvider( self, name, priority, getTypeId, getModel, getModelFromTypeId ):
		provider = LuaObjectModelProvider( name, priority, getTypeId, getModel, getModelFromTypeId )
		ModelManager.get().registerModelProvider( provider )
		self.modelProviders.append( provider )
		return provider

	def cleanLuaBridgeReference(self):
		for provider in self.modelProviders:
			provider.clear()
			ModelManager.get().unregisterModelProvider( provider )
		self.modelProviders = []

##----------------------------------------------------------------##

ModelBridge()

##----------------------------------------------------------------##