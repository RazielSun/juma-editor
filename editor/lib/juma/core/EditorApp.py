import os
import os.path
import sys
import logging
import platform
import time

import signals
import jsonHelper

import globalSignals
from EditorModule   import EditorModule, EditorModuleManager
from Project        import Project
# from package        import PackageManager
from MainModulePath import getMainModulePath
from Command        import EditorCommandRegistry

# from InstanceHelper import checkSingleInstance, setRemoteArgumentCallback, sendRemoteMsg

# _GII_BUILTIN_PACKAGES_PATH = 'packages'
# _GII_APP_CONFIG_FILE = 'config.json'

_JUMA_PROJECT_DEFAULT_SETTINGS = 'projectDefaults.json'

_JUMA_EDITOR_PATH = '/editor'

##----------------------------------------------------------------##
class EditorApp(object):
	_singleton = None

	@staticmethod
	def get():
		return _singleton

	def __init__(self):
		assert(not EditorApp._singleton)
		EditorApp._singleton = self
		EditorModuleManager.get()._app = self

		self.defaultMainloopBudget = 0.005

		self.initialized   = False
		self.projectLoaded = False
		# self.flagModified  = False
		# self.debugging     = False
		self.running       	= False
		self.appPath 		= getMainModulePath()
		self.basePath      	= self.appPath + _JUMA_EDITOR_PATH
		self.dataPaths     	= []
		self.config        	= {}
		self.settings 		= {}
		# self.packageManager   = PackageManager()

		self.commandRegistry       = EditorCommandRegistry.get()
		
		self.registerDataPath( self.getPath('data') )

		signals.connect( 'module.register', self.onModuleRegister )

	def onModuleRegister(self, m):		
		if self.running:
			logging.info('registered in runtime:'+m.getName())
			EditorModuleManager.get().loadModule(m)

	def init( self, **options ):
		# if options.get( 'stop_other_instance', False ):
		# 	if not checkSingleInstance():
		# 		retryCount = 5
		# 		logging.warning( 'running instance detected, trying to shut it down' )
		# 		sendRemoteMsg( 'shut_down' )
		# 		ready = False
		# 		for i in range( retryCount ):
		# 			time.sleep( 1 )
		# 			if checkSingleInstance():
		# 				ready = True
		# 				break
		# 		if not ready:
		# 			logging.warning( 'timeout for shuting down other instance' )
		# 			return False

		# else:
		# 	if not checkSingleInstance():
		# 		logging.warning( 'running instance detected' )
		# 		return False
		
		self.loadConfig()
		self.loadSettings()

		if self.initialized: return True
		self.openProject()
		
		# #scan packages
		# excludePackages = self.getProject().getConfig( 'excluded_packages' )
		# self.packageManager.addExcludedPackage( excludePackages )

		# if not self.packageManager.scanPackages( self.getPath( _GII_BUILTIN_PACKAGES_PATH ) ):
		# 	return False

		# if self.getProject().isLoaded():
		# 	self.packageManager.scanPackages( self.getProject().envPackagePath )

		# #modules
		EditorModuleManager.get().loadAllModules()
		signals.emitNow( 'module.loaded' ) #some pre app-ready activities
		signals.dispatchAll()

		# self.getProject().loadAssetLibrary()

		self.initialized = True
		self.running     = True

		# signals.connect( 'app.remote', self.onRemote )

		return True


	def run( self, **kwargs ):
		if not self.initialized: 
			if not self.init( **kwargs ):
				return False
		hasError = False
		self.resetMainLoopBudget()
		
		try:
			signals.emitNow('app.pre_start')

			EditorModuleManager.get().startAllModules()
	# 		self.getProject().getAssetLibrary().scanProject()

			signals.emitNow('app.start')
			signals.dispatchAll()

			self.saveConfig()

			EditorModuleManager.get().tellAllModulesAppReady()
			signals.emit('app.ready')

			#main loop
			while self.running:
				self.doMainLoop()

		except Exception, e:
			# TODO: popup a alert window?
			logging.exception( e )
			hasError = True

		signals.emitNow('app.close')

		signals.dispatchAll()
		EditorModuleManager.get().stopAllModules()
		
		if not hasError:
			self.getProject().save()
			self.getProject().saveConfig()

		signals.dispatchAll()
		EditorModuleManager.get().unloadAllModules()
		return True

	def setMainLoopBudget( self, budget = 0.001 ):
		self.mainLoopBudget = budget

	def resetMainLoopBudget( self ):
		return self.setMainLoopBudget( self.defaultMainloopBudget )

	def setMinimalMainLoopBudget( self ):
		return self.setMainLoopBudget( 0.001 )

	def doMainLoop( self ):
		budget = self.mainLoopBudget
		t0 = time.time()
		EditorModuleManager.get().updateAllModules()
		tx = time.time()
		if signals.dispatchAll():
			rest = 0
		else:
			t1 = time.time()
			elapsed = t1 - t0
			rest = budget - elapsed
		if rest > 0:
			time.sleep( rest )

	# def tryStop( self, timeout = 0 ):
	# 	#TODO: alert if any asset is not saved
	# 	self.stop()
	# 	return True

	def stop( self ):
		self.running = False
		self.saveConfig()

	def loadSettings( self ):
		loaded = jsonHelper.tryLoadJSON( self.getPath( 'data/' + _JUMA_PROJECT_DEFAULT_SETTINGS ) )
		if loaded:
			self.settings = loaded

	def getSetting( self, **options ):
		project = self.getProject()
		settingName = options.get("name", "None")
		hasItem = options.get("exists", None)

		projSetting = project.info.get(settingName, None)
		if projSetting:
			if hasItem:
				for st in projSetting:
					if st.get("name") == hasItem:
						return st
			else:
				return projSetting

		projSetting = self.settings.get(settingName, None)
		if hasItem:
			for st in projSetting:
				if st.get("name") == hasItem:
					return st
		else:
			return projSetting

	def saveConfig( self ):
		pass
		# jsonHelper.trySaveJSON( self.config, self.getPath( _GII_APP_CONFIG_FILE ), 'project config' )

	def loadConfig( self ):
		pass
	# 	loaded = jsonHelper.tryLoadJSON( self.getPath( _GII_APP_CONFIG_FILE ) )
	# 	if loaded:
	# 		config = self.config
	# 		for k, v in loaded.items():
	# 			config[ k ] = v
	# 	else:
	# 		self.saveConfig()

	# def setConfig( self, name, value, saveNow = True ):
	# 	self.config[name] = value
	# 	if saveNow:
	# 		self.saveConfig()

	# def getConfig( self, name, default = None ):
	# 	return self.config.get( name, default )

	# def affirmConfig( self, name, default = None ):
	# 	value = self.config.get( name, None )
	# 	if value == None:
	# 		self.config[ name ] = default
	# 		return default

	def getModule(self, name):
		return EditorModuleManager.get().getModule( name )

	def affirmModule(self, name):
		return EditorModuleManager.get().affirmModule( name )

	def createCommandStack( self, stackName ):
		return self.commandRegistry.createCommandStack( stackName )

	def getCommandStack( self, stackName ):
		return self.commandRegistry.getCommandStack( stackName )

	def clearCommandStack( self, stackName ):
		stack = self.commandRegistry.getCommandStack( stackName )
		if stack:
			stack.clear()

	def doCommand( self, fullname, *args, **kwargs ):
		return self.commandRegistry.doCommand( fullname, *args, **kwargs )

	def undoCommand( self, popOnly = False ):
		return self.commandRegistry.undoCommand( popOnly )

	def getPath( self, path = None ):
		if path:
			return self.basePath + '/' + path
		else:
			return self.basePath

	def getPythonPath( self ):
		return sys.executable

	def findDataFile( self, fileName ):
		for path in self.dataPaths:
			f = path + '/' + fileName
			if os.path.exists( f ):
				return f
		return None

	def registerDataPath( self, dataPath ):
		self.dataPaths.append( dataPath )

	def getProject( self ):
		return Project.get()

	def openProject( self, basePath = None ):
		proj = Project.get()
		if proj.load( basePath ):
			self.projectLoaded = True
	# 	if self.projectLoaded: return Project.get()
	# 	info = Project.findProject( basePath )
	# 	if not info:
	# 		raise Exception( 'no valid gii project found' )
	# 	proj = Project.get()
	# 	proj.load( info['path'] )
	# 	self.projectLoaded = True
	# 	self.registerDataPath( proj.getEnvPath('data') )
	# 	return proj

	def getAssetLibrary( self ):
		return self.getProject().getAssetLibrary()
	
	def getPlatformName( self ):
		name = platform.system()
		if name == 'Linux':
			return 'linux'
		elif name == 'Darwin':
			return 'osx'
		elif name == 'Windows':
			return 'win'
		else:
			raise Exception( 'what platform?' + name )

	def getRelPath( self, path ):
		proj = self.getProject()
		if proj:
			path = path.replace(proj.getPath(), "{project}")
		return path

	def getAbsPath( self, path ):
		proj = self.getProject()
		if proj:
			path = path.replace('{project}', proj.getPath())
		return path

##----------------------------------------------------------------##

app = EditorApp()
