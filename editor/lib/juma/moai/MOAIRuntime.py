
import os, sys
import logging
import os.path
import moaipy

from juma.core import signals, app, EditorModule
from moaipy import *

from exceptions import *
# from MOAIInputDevice import MOAIInputDevice
from LuaTableProxy   import LuaTableProxy

##----------------------------------------------------------------##
_G   		= LuaTableProxy( None )
_Runtime 	= LuaTableProxy( None )

# signals.register( 'lua.msg' )
# signals.register( 'moai.clean' )
# signals.register( 'moai.reset' )
# signals.register( 'moai.ready' )

signals.register( 'moai.open_window' )
signals.register( 'moai.set_sim_step' )

##----------------------------------------------------------------##
# import bridge


##----------------------------------------------------------------##
## MOAIRuntime
##----------------------------------------------------------------##
class MOAIRuntime( EditorModule ):
	_singleton = None

	_name       = 'moai'
	_dependency = []
	_initialized = False

	lua = None

	@staticmethod
	def get():
		return MOAIRuntime._singleton

	def __init__(self):
		assert not MOAIRuntime._singleton
		MOAIRuntime._singleton = self
		super(MOAIRuntime, self).__init__()	

		self.paused            	= False
		self.GLContextReady    	= False
		self.AKUReady			= False
		
		self.luaModules        	= []
		self.luaDelegates      	= {}

		self.inputDevices      	= {}
		self.lastInputDeviceId 	= 0

		self.simStep 			= 0

	##----------------------------------------------------------------##
	def getLuaEnv(self):
		return _G

	def getRuntimeEnv(self):
		return _Runtime

	#-------Context Control
	def initContext(self):
		global _G
		global _Runtime

		self.luaModules        = []

		self.inputDevices      = {}
		self.lastInputDeviceId = 0
		
		self.GLContextReady = False
		self.resetContext()

		AKUSetInputConfigurationName ( 'JUMA' )

		self.lua = LuaRuntime()
		self.lua.init()
		# inject python env
		_G._setTarget( self.lua.globals() )
		# _G['GII_PYTHON_BRIDGE']            = bridge
		# _G['GII_DATA_PATH']                = self.getApp().getPath('data')

		_G['LIB_LUA_PATH'] = self.getApp().getPath('lib/lua')

		self.runScript(
			self.getApp().getPath( 'lib/lua/init.lua' )
		)

		_Runtime._setTarget( _G['editor'] )

		assert _Runtime, "Failed loading Lua Runtime!"
		#finish loading lua bridge
		
		self.AKUReady      		= True
		# self.RunningScript = False
		self.paused        		= False
		# self.GLContextInitializer = None

	def initGLContext(self):
		if self.GLContextReady:
			return True

		from juma.qt.controls.GLWidget import GLWidget
		GLWidget.getSharedWidget().makeCurrent()

		AKUDetectGfxContext()
		self.GLContextReady = True
		return True

	def createContext(self):
		if not self._initialized:
			AKUAppInitialize ()
			AKUModulesAppInitialize ()
			self._initialized = True

		AKUCreateContext ()
		AKUModulesContextInitialize ()
		
		AKUInitializeCallbacks ()

		AKUSetInputConfigurationName ( "QtEditor" );

		AKUModulesRunLuaAPIWrapper ()
		AKUInitParticlePresets ()

		moaipy.callback_SetSimStep = self.setSimStep
		moaipy.callback_OpenWindow = self.openWindow		

	def destroyContext(self):
		context = AKUGetContext ()
		if context != 0:
			self.lua.destroy()
			self.lua = None
			AKUDeleteContext ( context )
			self.finalize()

	def resetContext(self):
		self.destroyContext()
		self.createContext()

	def finalize(self):
		AKUModulesAppFinalize ()	

##----------------------------------------------------------------##

	def openWindow(self, title, width, height):
		AKUDetectGfxContext()
		signals.emitNow( 'moai.open_window', title, width, height )
  		print("OPEN WINDOW: {} {} {}".format(title, width, height))

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
		_Runtime.createRenderContext( key, *clearColor )

	def changeRenderContext(self, contextId, w, h ):
		_Runtime.changeRenderContext( contextId or False, w or False, h or False )

##----------------------------------------------------------------##
	def onLoad(self):
		self.AKUReady = False
		self.initContext()
		# self.setWorkingDirectory( self.getProject().getPath() )
		self.initGLContext()

	def onUnload(self):
		self.AKUReady   = False

MOAIRuntime().register()
