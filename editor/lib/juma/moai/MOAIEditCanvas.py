import os.path
import time
from time import time as getTime

from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt

from juma import *

from juma.qt.controls.GLWidget 	import GLWidget
from MOAIRuntime              	import MOAIRuntime, MOAILuaDelegate
from MOAICanvasBase           	import MOAICanvasBase



##----------------------------------------------------------------##
class MOAIEditCanvasLuaDelegate( MOAILuaDelegate ):
	def load(self, scriptPath, scriptEnv = None ):
		super( MOAIEditCanvasLuaDelegate, self ).load( scriptPath, scriptEnv )



##----------------------------------------------------------------##
class MOAIEditCanvasBase( MOAICanvasBase ):
	_id = 0
	def __init__( self, *args, **kwargs ):
		MOAIEditCanvas._id += 1
		super(MOAIEditCanvasBase, self).__init__( *args )

		self.enabled = False

		contextPrefix = kwargs.get( 'context_prefix', 'edit_canvas')
		self.clearColor  = kwargs.get( 'clear_color', ( 0, 0, 0, 1 ) )
		self.runtime     = app.affirmModule( 'moai' )
		self.contextName = '%s<%d>' % ( contextPrefix, MOAIEditCanvas._id )
		self.delegate    = MOAIEditCanvasLuaDelegate( self, autoReload = False )
		self.updateTimer = QtCore.QTimer(self)
		self.viewWidth   = 0
		self.viewHeight  = 0
		
		self.scriptEnv   = None
		self.scriptPath  = None
		self.lastUpdateTime = 0 
		self.updateStep  = 0
		self.alwaysForcedUpdate = False

		# self.currentCursorId = 'arrow'
		# self.cursorHidden = False

		self.updateTimer.timeout.connect( self.updateCanvas )

		signals.connect('moai.reset', self.onMoaiReset)
		signals.connect('moai.clean', self.onMoaiClean)

	def startUpdateTimer( self, fps = 60 ):
		self.enabled = True
		step = 1.0 / fps
		self.updateTimer.start( 1000 * step )
		self.updateStep = step
		self.lastUpdateTime = getTime()

	def stopUpdateTimer(self):
		self.enabled = False
		self.updateTimer.stop()

	def loadScript( self, scriptPath, env = None, **kwargs ):
		self.scriptPath = scriptPath
		self.scriptEnv  = env
		self.setupContext()

	def setupContext(self):
		self.runtime.createRenderContext( self.contextName, self.clearColor )
		
		if self.scriptPath:
			self.makeCurrent()
			env = {
			}
		# 		'updateCanvas'     : boundToClosure( self.updateCanvas ),
		# 		'hideCursor'       : boundToClosure( self.hideCursor ),
		# 		'showCursor'       : boundToClosure( self.showCursor ),
		# 		'setCursor'        : boundToClosure( self.setCursorById ),
		# 		'setCursorPos'     : boundToClosure( self.setCursorPos ),
		# 		'getCanvasSize'    : boundToClosure( self.getCanvasSize ),
		# 		'startUpdateTimer' : boundToClosure( self.startUpdateTimer ),
		# 		'stopUpdateTimer'  : boundToClosure( self.stopUpdateTimer ),
		# 		'contextName'      : boundToClosure( self.contextName )				
		# 	}
			
			if self.scriptEnv:
				env.update( self.scriptEnv )
			self.delegate.load( self.scriptPath, env )

			self.delegate.safeCall( 'onLoad' )
			self.resizeGL(self.width(), self.height())
			self.startRefreshTimer()
			self.startUpdateTimer() # FIXME
			self.updateCanvas()

	def makeCurrent( self ):
		self.runtime.changeRenderContext( self.contextName, self.viewWidth, self.viewHeight )

	def onMoaiReset( self ):
		self.setupContext()

	def onMoaiClean(self):
		self.stopUpdateTimer()
		self.stopRefreshTimer()

	def onDraw(self):
		runtime = self.runtime
		runtime.setBufferSize( self.viewWidth, self.viewHeight )
		self.makeCurrent()
		runtime.manualRenderAll()
		# self.delegate.postDraw()

	def updateCanvas( self, **option ):
		currentTime = getTime()
		step = currentTime - self.lastUpdateTime
		self.lastUpdateTime = currentTime
		
		step = self.updateStep #>>>>>>

		runtime = self.runtime
		runtime.setBufferSize( self.viewWidth, self.viewHeight )

		# if not option.get( 'no_sim', False ):	
		# 	runtime.stepSim( step )
		# 	getAKU().updateFMOD()

		# self.delegate.onUpdate( step )
		if self.runtime.updateAKU(): # FIXME
			if option.get( 'forced', self.alwaysForcedUpdate ):
				self.forceUpdateGL()
			else:
				self.updateGL()

	# change
	def resizeGL(self, width, height):
		# self.delegate.onResize(width,height)
		print("resizeGL: {} {}".format(width, height))
		self.viewWidth  = width
		self.viewHeight = height



##----------------------------------------------------------------##
class MOAIEditCanvas( MOAIEditCanvasBase ):
	def __init__( self, *args, **kwargs ):
		super( MOAIEditCanvas, self ).__init__( *args, **kwargs )
		# self.keyGrabbingCount = 0