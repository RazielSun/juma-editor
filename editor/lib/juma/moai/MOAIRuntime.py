
import os, sys
import logging
import os.path
import moaipy

from juma.core 	import signals, app, EditorModule
from moaipy 	import *

from exceptions 		import *
from MOAIInputDevice 	import MOAIInputDevice
from LuaTableProxy   	import LuaTableProxy
from LuaPrint			import printSeparator, printTraceBack

##----------------------------------------------------------------##
_G   			= LuaTableProxy( None )
_Render 		= LuaTableProxy( None )

# signals.register( 'lua.msg' )

signals.register( 'moai.prepare_clean' )
signals.register( 'moai.clean' )
signals.register( 'moai.reset' )
signals.register( 'moai.ready' )
signals.register( 'framework.init' )

signals.register( 'moai.open_window' )
signals.register( 'moai.set_sim_step' )

##----------------------------------------------------------------##
import bridge

##----------------------------------------------------------------##
## MOAIRuntime
##----------------------------------------------------------------##
class MOAIRuntime( EditorModule ):
	_singleton = None
	@staticmethod
	def get():
		return MOAIRuntime._singleton

	_name       = 'moai'
	_dependency = []

	def __init__(self):
		assert not MOAIRuntime._singleton
		MOAIRuntime._singleton = self
		super(MOAIRuntime, self).__init__()	

		self.paused            	= False
		self.GLContextReady    	= False
		self.AKUReady			= False
		self.lua 				= None
		
		self.luaModules        	= []
		self.luaDelegates      	= {}

		self.inputDevices      	= {}
		self.lastInputDeviceId 	= 0

		self.simStep 			= 0
		
		signals.connect( 'project.load', self.onProjectLoaded )

	##----------------------------------------------------------------##
	def getLuaEnv(self):
		return _G

	#-------Context Control
	def initContext(self):
		global _G
		global _Render

		self.luaModules        = []

		self.inputDevices      = {}
		self.lastInputDeviceId = 0
		
		self.GLContextReady = False
		self.resetContext()

		self.lua = LuaRuntime()
		self.lua.init()

		moaipy.callback_SetSimStep = self.setSimStep
		moaipy.callback_OpenWindow = self.openWindow

		### inject python env
		_G._setTarget( self.lua.globals() )

		_G['PYTHON_BRIDGE']            	= bridge
		_G['LIB_JUMA_LUA_PATH'] 		= self.getApp().getPath('lib/lua/juma')
		_G['LIB_EDITOR_LUA_PATH'] 		= self.getApp().getPath('lib/lua/editor')
		_G['LIB_FRAMEWORK_LUA_PATH'] 	= self.getApp().getPath('lib/lua/framework/src')

		self.addDefaultInputDevice( 'device' )
		self.runScript( self.getApp().getPath( 'lib/lua/juma/init.lua' ) )

		_Render._setTarget( _G['RenderContextMgr'] )
		assert _Render, "Failed loading Editor!"
		### finish loading lua bridge
		
		self.AKUReady      		= True
		self.paused        		= False

	def initGLContext(self):
		if self.GLContextReady:
			return True

		from juma.qt.controls.GLWidget import GLWidget
		GLWidget.getSharedWidget().makeCurrent()

		AKUDetectGfxContext()
		self.GLContextReady = True
		return True

	def createContext(self):
		AKUAppInitialize ()
		AKUModulesAppInitialize ()

		AKUCreateContext ()
		AKUModulesContextInitialize ()
		
		AKUInitializeCallbacks ()

		AKUSetInputConfigurationName ( 'JUMA' )

		AKUModulesRunLuaAPIWrapper ()
		AKUInitParticlePresets ()

	def destroyContext(self):
		context = AKUGetContext ()
		if context != 0:
			global _G
			global _Render
			_G._setTarget( None )
			_Render._setTarget( None )
			self.lua = None
			AKUDeleteContext ( context )

	def resetContext(self):
		self.destroyContext()
		self.createContext()

	def runGame(self):
		if self.getProject().isLoaded():
			filename = "main.lua"
			path = self.getProject().gamePath
			printSeparator( path, filename )
			self.setWorkingDirectory( path )
			self.runScript( filename )

	def reset(self):
		if not self.AKUReady: return
		self.cleanLuaReferences()
		self.setup()

		signals.emitNow( 'moai.reset' )
		signals.emitNow( 'moai.ready' )

	def setup(self):
		self.initContext()
		self.setWorkingDirectory( self.getApp().getPath() )
		self.initGLContext()

	def finalize(self):
		AKUModulesAppFinalize ()
		AKUAppFinalize ()

	####  LuaModule Related
	def registerLuaModule(self, m):
		self.luaModules.append(m)
		registerModule(m)
	
	# clean holded lua object(this is CRITICAL!!!)
	def cleanLuaReferences(self):
		signals.emitNow( 'moai.prepare_clean' )
		for m in self.luaModules:
			unregisterModule(m)

		bridge.clearSignalConnections()
		bridge.clearLuaRegisteredSignals()

		introspector = self.getModule('introspector')
		if introspector:
			instances = introspector.getInstances()
			for ins in instances:
				if isinstance(ins.target,(moaipy._LuaTable, moaipy._LuaObject, moaipy._LuaThread, moaipy._LuaFunction)):
					ins.clear()

		signals.emitNow( 'moai.clean' )

##----------------------------------------------------------------##
## Input Device Management
##----------------------------------------------------------------##
	def getInputDevice(self, name='device'):
		return self.inputDevices.get(name, None)

	def addInputDevice(self, name):
		device = MOAIInputDevice( name, self.lastInputDeviceId )
		self.inputDevices[name] = device
		self.lastInputDeviceId += 1

		AKUReserveInputDevices ( self.lastInputDeviceId )
		for inputDevice in self.inputDevices.values():
			inputDevice.onRegister()
		return device

	def addDefaultInputDevice( self, name='device' ):
		device = self.addInputDevice( name )
		# device.addSensor('touch',       'touch')
		device.addSensor('pointer',     'pointer')
		device.addSensor('keyboard',    'keyboard')
		device.addSensor('mouseLeft',   'button')
		device.addSensor('mouseRight',  'button')
		device.addSensor('mouseMiddle', 'button')
		# for i in range( 0, 4 ):
		# 	device.addJoystickSensors( i + 1 )
		return device

##----------------------------------------------------------------##
	def openWindow(self, title, width, height):
		AKUDetectGfxContext()
		signals.emitNow( 'moai.open_window', title, width, height )

	def setSimStep(self, step):
		self.simStep = step
		signals.emitNow( 'moai.set_sim_step', step )

	def setWorkingDirectory(self, path):
		AKUSetWorkingDirectory ( path )

	def pause(self, paused=True):
		self.paused = paused
		AKUPause ( self.paused )

	def resume(self):
		self.pause(False)

	def updateAKU(self):
		if not self.AKUReady:
			return False
		if self.paused:
			return False
		AKUModulesUpdate ()
		return True

	def renderAKU(self):
		if not self.AKUReady:
			return False
		AKURender ()
		return True

	def runScript(self, fileName):
		AKURunScript ( fileName )

	def runString(self, luaStr):
		AKURunString ( luaStr )

	def setScreenSize(self, width, height):
		AKUSetScreenSize ( width, height )

	def setViewSize(self, width, height):
		AKUSetViewSize ( width, height )

##----------------------------------------------------------------##
	def createRenderContext( self, key, clearColor = (0,0,0,0) ):
		_Render.createRenderContext( key, *clearColor )

	def changeRenderContext( self, contextId, w, h ):
		_Render.changeRenderContext( contextId or False, w or False, h or False )

	def setBufferSize( self, width, height ):
		_Render.setBufferSize( width, height )

	def manualRender( self ):
		if not self.GLContextReady:
			return
		_Render.manualRender()

	def refreshAssets( self ):
		_G.refreshAssets()

	def getEditorCommand( self, name ):
		return _G.getEditorCommandRegistry( name )

	def getLuaClassRegistry( self, classType ):
		return _G.getEditorRegistry( classType )

	def updateStepSim( self, step ):
		try:
			_G.updateStepSim( step )
		except Exception, e:
			logging.error( 'error loading lua:\n' + str(e) )

	def takeScreenshot( self ):
		try:
			_G.takeScreenshot()
		except Exception, e:
			logging.error( 'error loading lua:\n' + str(e) )

	def garbageCollect( self ):
		try:
			_G.garbageCollect()
		except Exception, e:
			logging.error( 'error loading lua:\n' + str(e) )

	def setLuaEnvResolution( self, width, height ):
		try:
			_G.setGameResolution( width, height )
		except Exception, e:
			logging.error( 'error loading lua:\n' + str(e) )

	def loadLuaDelegate( self, file, env = None, **option ):
		try:
			if env:
				assert isinstance( env, dict )
			return _G.loadLuaDelegate( file, env, option.get( 'isdelegate', False ) )
		except Exception, e:
			logging.error( 'error loading lua:\n' + str(e) )

##----------------------------------------------------------------##
	def onProjectLoaded(self, project):
		self.reset()

	def onLoad(self):
		self.AKUReady = False
		self.setup()

	def onAppReady(self):
		signals.emitNow( 'framework.init' )

	def onUnload(self):
		self.AKUReady   = False

##----------------------------------------------------------------##

MOAIRuntime().register()

##----------------------------------------------------------------##
## Delegate
##----------------------------------------------------------------##
class MOAILuaDelegate(object):
	def __init__(self, owner=None, **option):
		self.scriptPath   = None
		self.scriptEnv    = None
		self.owner        = owner
		self.name         = option.get( 'name', None )

		self.extraSymbols = {}
		self.clearLua()

		signals.connect('moai.clean', self.clearLua)
		if option.get( 'autoReload', True ):
			signals.connect('moai.reset', self.reload)

	def load( self, scriptPath, scriptEnv = None ):
		self.scriptPath = scriptPath
		self.scriptEnv  = scriptEnv
		runtime = MOAIRuntime.get()
		try:
			env = {
				'_owner'      : self.owner,
				'_delegate'   : self
			}
			if self.scriptEnv:
				env.update( self.scriptEnv )
			if self.name:
				env['_NAME'] = env.name
			self.luaEnv = runtime.loadLuaDelegate( scriptPath, env, isdelegate = True )
		except Exception, e:
			logging.exception( e )

	def reload(self):
		if self.scriptPath: 
			self.load( self.scriptPath, self.scriptEnv )
			for k,v in self.extraSymbols.items():
				self.setEnv(k,v)

	def setEnv(self, name ,value, autoReload = True):
		if autoReload : self.extraSymbols[name] = value
		self.luaEnv[name] = value

	def getEnv(self, name, defaultValue = None):
		v = self.luaEnv[name]
		if v is None : return defaultValue
		return v

	def safeCall(self, method, *args):
		if not self.luaEnv:
			printTraceBack()
			logging.error( 'trying call a empty lua delegate, owned by %s' % repr( self.owner ) )
			return
		m = self.luaEnv[method]
		if not m: return
		try:
			return m(*args)
		except Exception, e:
			# logging.exception( e )
			print e
	
	def safeCallMethod( self, objId, methodName, *args ):
		if not self.luaEnv: 
			printTraceBack()
			logging.error( 'trying call a empty lua delegate, owned by %s' % repr( self.owner ) )
			return
		obj = self.luaEnv[objId]
		if not obj: return
		method = obj[methodName]
		if not method: return
		try:
			return method( obj, *args )
		except Exception, e:
			# logging.exception( e )
			print e

	def call(self, method, *args):
		m = self.luaEnv[method]
		return m(*args)

	def callMethod( self, objId, methodName, *args ):
		obj = self.luaEnv[objId]
		method = obj[methodName]
		return method( obj, *args )

	def clearLua(self):
		self.luaEnv=None