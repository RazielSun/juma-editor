import logging

##----------------------------------------------------------------##
def getSuperType( t ):
	if isinstance( t, DataType ):
		return t.getSuperType()
		
	m = ModelManager._singleton.getModelFromTypeId( t )
	if m:
		return m.getSuperType()
	return None

##----------------------------------------------------------------##
class DataType(object):
	def getName(self):
		return None

	def getSuperType( self ):
		return None

	def getDefaultValue(self):
		return None
	
	def repr(self, value):
		return repr(value)

	def check(self, value):
		return value

	def serialize(self, value):
		raise 'not implemented'

	def deserialize(self, data):
		raise 'not implemlented'

	def register( self ):
		raise 'not implemented'

##----------------------------------------------------------------##
class PythonValueType(DataType):
	def __init__(self ,t, defaultValue):
		self._type = t
		name = repr(t)
		self._defaultValue = defaultValue

	def getName(self):
		return repr(self._type)

	def check(self, value):
		if value is self._type:
			return value
		return None

	def register( self, typeId ):
		ModelManager.get().registerPythonModel( typeId, self )
		return self

##----------------------------------------------------------------##
class EnumType( DataType ):
	def __init__( self, name, enum, defaultValue = None ):
		self.name = name
		itemDict = {}

		self.itemDict = itemDict
		for item in enum:
			( name, value ) = item
			itemDict[ name ] = value
		self._defaultValue = defaultValue
		self.itemList = enum[:]

	def getName( self ):
		return self.name

	def getSuperType( self ):
		return EnumType

	def repr( self, value ):
		return '<%s> %s' %( self.name, repr( value ) )

	def fromIndex( self, idx ):
		if idx < 0 or idx >= len( self.itemList ):
			return None
		( name, value ) = self.itemList[ idx ]
		return value

	def toIndex( self, value ):
		for i, item in enumerate( self.itemList ):
			( k, v ) = item
			if value == v: return i
		return None

	def getItemList( self, contextObject ):
		return self.itemList

##----------------------------------------------------------------##
class AssetRefType( DataType ):
	def __init__( self, assetType ):
		self.assetType = assetType

	def getName( self ):
		return self.assetType

	def getAssetType( self, contextObject ):
		atype = self.assetType
		if isinstance( atype, ( str, unicode ) ):
			return atype
		else: #asset type getter function
			return atype( contextObject )

	def getSuperType( self ):
		return AssetRefType

	def repr( self, value ):
		return '<%s> %s' % ( self.assetType, value )

##----------------------------------------------------------------##
class ArrayType( DataType ):
	def __init__(self, name, itemType, defaultValue = None ):
		self.name = name
		self.itemType = itemType	
		
	def getName( self ):
		return self.name

	def getSuperType( self ):
		return ArrayType

	def repr( self, value ):
		return '<%s> %s' %( self.name, repr( value ) )
		
##----------------------------------------------------------------##
class CollectionType( DataType ):
	def __init__(self, name, itemType, defaultValue = None ):
		self.name = name
		self.itemType = itemType	
		
	def getName( self ):
		return self.name

	def getSuperType( self ):
		return CollectionType

	def repr( self, value ):
		return '<%s> %s' %( self.name, repr( value ) ) 

##----------------------------------------------------------------##
class ObjectModel(DataType):
	def __init__(self, name, superType = None, **option):
		self.name      = name
		self.fieldMap  = {}
		self.fieldList = []
		self.superType = None
		if superType:
			self.setSuperType( superType )

	def addFieldInfo(self, id, t, **option):
		f = self.createField(id, t, **option)
		self.fieldMap[id] = f
		self.fieldList.append(f)
		return f

	def getFieldInfo(self, id):
		return self.fieldMap.get(id, None)

	def createField( self, id, t, **option ):
		return Field(self, id, t, **option)

	def getFieldValue(self, obj, id):
		f=self.getFieldInfo(id)
		return f.getValue(obj)

	def setFieldValue(self, obj, id, value):
		f = self.getFieldInfo(id)
		f.setValue(obj, value)

	def calculateField(self, obj, id):
		f = self.getFieldInfo(id)
		f.calculate(obj)

	def isFieldOverrided( self, obj, id ):
		return False

##----------------------------------------------------------------##
class Field(object):
	def __init__(self, model, id, _type, **option):
		self._type = _type
		self.model = model
		self.id    = id
		option = option or {}
		self.label	   = option.get( 'label',    id )
		self.default   = option.get( 'default',  None )
		self.getter	   = option.get( 'get',      True )
		self.setter	   = option.get( 'set',      True )
		self.calculate = option.get( 'calc', 	 False )
		self.readonly  = option.get( 'readonly', False )
		if self.setter == False: self.readonly = True
		option[ 'readonly' ] = self.readonly
		self.option    = option

	def __repr__( self ):
		return 'field: %s <%s>' % ( self.id, repr(self._type) )

	def getType( self ):
		return self._type

	def getOption( self, key, default = None ):
		return self.option.get( key, default )

	def getValue( self, obj, defaultValue = None ):
		getter = self.getter
		if getter == False: return None
		if getter == True: # indexer
			if isinstance( obj, dict ):
				return obj.get( self.id, defaultValue )
			else:
				return getattr( obj, self.id, defaultValue )
		v = self.getter( obj, self.id ) # caller
		if v is None: return defaultValue
		return v

	def setValue( self, obj, value ):
		if self.readonly: return 
		if self.setter == True:
			if isinstance( obj, dict ):
				obj[ self.id ] = value
			else:
				setattr(obj, self.id, value)
		else:
			self.setter(obj, value)

	def calculate( self, obj ):
		if self.readonly: return 
		if self.calculate:
			self.calculate(obj)

##----------------------------------------------------------------##
## ModelManager
##----------------------------------------------------------------##
class ModelProvider(object):
	def getModel( self, obj ):
		return None

	def getTypeId( self, obj ):
		return None

	def getModelFromTypeId( self, typeId ):
		return None

	def getPriority( self ): 
		return 0 #the bigger the first

	def clear( self ):
		pass

##----------------------------------------------------------------##
class PythonModelProvider(ModelProvider):
	def __init__(self):
		self.typeMapV           = {}
		self.typeMapN           = {}

		self.registerModel( int,   PythonValueType( int,    0 ) )
		self.registerModel( float, PythonValueType( float,  0 ) )
		self.registerModel( str,   PythonValueType( str,    '' ) )
		self.registerModel( bool,  PythonValueType( bool,   False ) )

	def registerModel(self, t, model):
		self.typeMapV[t]=model
		self.typeMapN[model.getName()]=model
		return model

	def unregisterModel(self, t, Model):
		del self.typeMapV[t]
		del self.typeMapN[Model.getName()]

	def getModel( self, obj ):
		return self.getModelFromTypeId( self.getTypeId(obj) )

	def getTypeId( self, obj ):
		typeId = type(obj)
		return typeId

	def getModelFromTypeId( self, typeId ):
		if typeId:
			return self.typeMapV.get( typeId, None )
		return None

##----------------------------------------------------------------##
class ModelManager(object):
	_singleton=None

	@staticmethod
	def get():
		return ModelManager._singleton

	def __init__(self):
		assert(not ModelManager._singleton)
		ModelManager._singleton = self

		self.modelProviders = []
		self.pythonModelProvider = self.registerModelProvider( PythonModelProvider() )

	def registerModelProvider( self, provider ):
		priority = provider.getPriority()
		for i, p in enumerate( self.modelProviders ):
			if priority >= p.getPriority() :
				self.modelProviders.insert( i, provider )
				return provider
		self.modelProviders.append( provider )
		return provider

	def unregisterModelProvider( self, provider ):
		idx = self.modelProviders.index( provider )
		self.modelProviders.pop( idx )

	def registerPythonModel(self, typeId, model):
		self.pythonModelProvider.registerModel( typeId, model)

	def getTypeId(self, obj):
		for provider in self.modelProviders:
			typeId = provider.getTypeId( obj )
			if typeId: return typeId			
		return None

	def getModel(self, obj):
		for provider in self.modelProviders:
			model = provider.getModel( obj )
			if model: return model			
		return None

	def getModelFromTypeId(self, typeId):
		for provider in self.modelProviders:
			model = provider.getModelFromTypeId( typeId )
			if model: return model
		return None
		
##----------------------------------------------------------------##

ModelManager()

##----------------------------------------------------------------##