import logging

##----------------------------------------------------------------##
class DataType(object):
	pass

##----------------------------------------------------------------##
class ObjectModel(DataType):
	pass

##----------------------------------------------------------------##
class Attr(object):
	pass

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
		pass

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