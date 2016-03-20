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
def luaTypeToPyType( tname ):
		if tname   == 'int':
			return int
		elif tname == 'string':
			return str
		elif tname == 'number':
			return float
		elif tname == 'boolean':
			return bool
		elif tname == 'nil':
			return None
		return tname

def luaTableToDict( luat, deepCopy = False ): #no deep conversion
	assert isinstance(luat , moaipy._LuaTable)
	res={}
	if deepCopy:
		for k in luat:
			v = luat[k]
			if isinstance( v, moaipy._LuaTable ):
				v = luaTableToDict( v, deepCopy )
			res[k] = v
	else:
		for k in luat:
			res[k] = luat[k]
	return res

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
class LuaObjectField( Field ):
	def __init__( self, model, id, _type, **option ):
		super( LuaObjectField, self ).__init__( model, id, _type, **option )
		if self.getter == False:
			self.getValue = self._getValueNone
		elif self.getter == True: 
			self.getValue = self._getValueRaw
		else:
			self.getValue = self._getValueGetter

		if self.readonly:
			self.setValue = self._setValueNone
		elif self.setter == True:
			self.setValue = self._setValueRaw
		else:
			self.setValue = self._setValueSetter
	
	def _getValueNone( self, obj, defaultValue = None ):
		return None

	def _getValueRaw( self, obj, defaultValue = None ):
		return getattr( obj, self.id, defaultValue )

	def _getValueGetter( self, obj, defaultValue = None ):
		v = self.getter( obj, self.id )
		if v is None: return defaultValue
		return v

	def _setValueNone( self, obj, value ):
		pass

	def _setValueRaw( self, obj, value ):
		setattr( obj, self.id, value )

	def _setValueSetter( self, obj, value ):
		if isinstance(value, tuple):
			self.setter(obj, *value)
		else:
			self.setter(obj, value)

##----------------------------------------------------------------##
class LuaObjectModel(ObjectModel):
	def __init__( self, name ):
		self.name = name

	def createField( self, id, t, **option ):
		return LuaObjectField(self, id, t, **option)

	# CALLED BY LUA
	def addLuaFieldInfo(self, name, typeId, data = None):
		typeId  = luaTypeToPyType( typeId ) # convert lua-typeId -> pythontype
		setting = data and luaTableToDict(data) or {}
		return self.addFieldInfo( name, typeId, **setting )

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
		return LuaObjectModel(name)

	def buildLuaObjectModelProvider( self, name, priority, getTypeId, getModel, getModelFromTypeId ):
		provider = LuaObjectModelProvider( name, priority, getTypeId, getModel, getModelFromTypeId )
		ModelManager.get().registerModelProvider( provider )
		self.modelProviders.append( provider )
		return provider

	def cleanLuaBridgeReference(self):
		for provider in self.modelProviders:
			# provider.clear()
			ModelManager.get().unregisterModelProvider( provider )
		self.modelProviders = []

##----------------------------------------------------------------##

ModelBridge()

##----------------------------------------------------------------##