import logging
import json
import weakref
import base64
import moaipy

from exceptions import *
from juma.core  import *
from moaipy 	import *

from juma.core.SelectionManager import getSelectionManager

##----------------------------------------------------------------##
def emitPythonSignal(name, *args):	
	signals.emit(name, *args)

def emitPythonSignalNow(name, *args):	
	signals.emitNow(name, *args)

##----------------------------------------------------------------##

def newPythonList(*arg):
	return list(arg)

def newPythonDict():
	return {}

def appendPythonList(list, data):
	list.append(data)
	
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

def sizeOfPythonObject(list):
	return len(list)

##----------------------------------------------------------------##
def getSelection( key ):
	selectionManager = getSelectionManager( key )
	s = selectionManager.getSelection()
	return s

def changeSelection( key, targets = None ):
	selectionManager = getSelectionManager( key )
	selectionManager.changeSelection( targets )

def addSelection( key, targets = None ):
	selectionManager = getSelectionManager( key )
	selectionManager.addSelection( targets )

def toggleSelection( key, targets = None ):
	selectionManager = getSelectionManager( key )
	selectionManager.toggleSelection( targets )

def removeSelection( key, targets = None ):
	selectionManager = getSelectionManager( key )
	selectionManager.removeSelection( targets )

##----------------------------------------------------------------##
def registerAssetNodeInLibrary( nodePath, assetType ):
	node = AssetNode( nodePath, assetType )
	AssetLibrary.get().registerAssetNode( node )

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
	_EnumCache = weakref.WeakValueDictionary()
	
	def createField( self, id, t, **option ):
		return LuaObjectField(self, id, t, **option)

	# CALLED BY LUA
	def addLuaFieldInfo(self, name, typeId, data = None):
		typeId  = luaTypeToPyType( typeId ) # convert lua-typeId -> pythontype
		setting = data and luaTableToDict(data) or {}
		return self.addFieldInfo( name, typeId, **setting )

	def addLuaEnumFieldInfo(self, name, enumItems, data = None):
		enumType = LuaObjectModel._EnumCache.get( enumItems, None )
		if not enumType:
			tuples = []
			for item in enumItems.values():
				itemName  = item[1]
				itemValue = item[2]
				tuples.append ( ( itemName, itemValue ) )
			enumType = EnumType( '_LUAENUM_', tuples )
			LuaObjectModel._EnumCache[ enumItems ] = enumType
		return self.addLuaFieldInfo( name, enumType, data )

	def addLuaAssetFieldInfo(self, name, assetType, data = None):
		typeId = AssetRefType( assetType )
		return self.addLuaFieldInfo( name, typeId, data )

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
			provider.clear()
			ModelManager.get().unregisterModelProvider( provider )
		self.modelProviders = []

##----------------------------------------------------------------##

ModelBridge()

##----------------------------------------------------------------##
class SafeDict(object):
	def __init__( self, dict ):
		self.__dict = dict

	def __setitem__( self, key, value ):
		self.__dict[key] = value

	def __getitem__( self, key ):
		return self.__dict.get( key, None )

	def __iter__( self ):
		return self.__dict

	def values( self ):
		return self.__dict.values()

##----------------------------------------------------------------##
def registerLuaEditorCommand( fullname, cmdCreator ):
	class LuaEditorCommand( EditorCommand ):	
		name = fullname
		def __init__( self ):
			self.luaCmd = cmdCreator()

		def __repr__( self ):
			cmd = self.luaCmd
			return cmd.toString( cmd )

		def init( self, **kwargs ):
			cmd = self.luaCmd
			return cmd.setup( cmd, SafeDict( kwargs ) )

		def redo( self ):
			cmd = self.luaCmd
			return cmd.redo( cmd )

		def undo( self ):
			cmd = self.luaCmd
			return cmd.undo( cmd )

		def canUndo( self ):
			cmd = self.luaCmd
			return cmd.canUndo( cmd )

		def hasHistory( self ):
			cmd = self.luaCmd
			return cmd.hasHistory( cmd )

		def getResult( self ):
			cmd = self.luaCmd
			return cmd.getResult( cmd )

		def getLuaCommand( self ):
			return self.luaCmd
			
	return LuaEditorCommand

##----------------------------------------------------------------##
def doCommand( cmdId, argTable ):
	pyArgTable = luaTableToDict( argTable )
	return app.doCommand( cmdId, **pyArgTable )

def undoCommand( popOnly = False ):
	return app.undoCommand( popOnly )