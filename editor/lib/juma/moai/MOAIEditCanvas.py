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
	def clearLua(self):
		super(MOAIEditCanvasLuaDelegate, self).clearLua()
		self._onMouseDown  = None
		self._onMouseUp    = None
		self._onMouseMove  = None
		self._onMouseEnter = None
		self._onMouseLeave = None
		self._onMouseScroll= None
		self._onKeyDown    = None
		self._onKeyUp      = None

		self._onResize     = None
		self._postDraw     = None
		self._onUpdate     = None

	def load(self, scriptPath, scriptEnv = None ):
		super( MOAIEditCanvasLuaDelegate, self ).load( scriptPath, scriptEnv )
		env = self.luaEnv
		if not env:
			raise Exception( 'failed loading editcanvas script:%s' % scriptPath )
		self.updateHooks()

	def updateHooks( self ):
		env = self.luaEnv
		if not env: return
		self._onMouseDown  = env.onMouseDown
		self._onMouseUp    = env.onMouseUp
		self._onMouseMove  = env.onMouseMove
		self._onMouseLeave = env.onMouseLeave
		self._onMouseEnter = env.onMouseEnter

		self._onMouseScroll= env.onMouseScroll
		self._onKeyDown    = env.onKeyDown
		self._onKeyUp      = env.onKeyUp

		self._onResize     = env.onResize
		self._postDraw     = env.postDraw
		self._onUpdate     = env.onUpdate

	def onMouseDown(self, btn, x,y):
		if self._onMouseDown:	self._onMouseDown(btn, x,y)

	def onMouseUp(self, btn, x,y):
		if self._onMouseUp: self._onMouseUp(btn, x,y)

	def onMouseMove(self, x,y):
		if self._onMouseMove: self._onMouseMove(x,y)

	def onMouseEnter(self):
		if self._onMouseEnter: self._onMouseEnter()

	def onMouseLeave(self):
		if self._onMouseLeave: self._onMouseLeave()

	def onMouseScroll(self, dx, dy, x, y):
		if self._onMouseScroll: self._onMouseScroll(dx,dy,x,y)

	def onKeyDown(self, key):
		if self._onKeyDown: self._onKeyDown(key)

	def onKeyUp(self, key):
		if self._onKeyUp: self._onKeyUp(key)
	
	def onUpdate(self, step):
		if self._onUpdate: self._onUpdate(step)

	def postDraw(self):
		if self._postDraw: self._postDraw()

	def onResize(self,w,h):
		if self._onResize: self._onResize(w,h)



##----------------------------------------------------------------##
class MOAIEditCanvasBase( MOAICanvasBase ):
	_id = 0
	def __init__( self, *args, **kwargs ):
		MOAIEditCanvas._id += 1
		super(MOAIEditCanvasBase, self).__init__( *args )

		self.enabled = False

		contextPrefix = kwargs.get( 'context_prefix', 'edit_canvas')
		self.clearColor  = kwargs.get( 'clear_color', ( 0, 0, 0, 0 ) )
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
		self.makeCurrent()
		runtime.setBufferSize( self.viewWidth, self.viewHeight )
		runtime.manualRender()
		self.delegate.postDraw()

	def updateCanvas( self, **option ):
		currentTime = getTime()
		step = currentTime - self.lastUpdateTime
		self.lastUpdateTime = currentTime
		
		step = self.updateStep #>>>>>>

		runtime = self.runtime
		runtime.setBufferSize( self.viewWidth, self.viewHeight )

		if not option.get( 'no_sim', False ):	
			runtime.updateStepSim( step )
		# 	getAKU().updateFMOD()

		self.delegate.onUpdate( step )
		if option.get( 'forced', self.alwaysForcedUpdate ):
			self.forceUpdateGL()
		else:
			self.updateGL()

	# change
	def resizeGL(self, width, height):
		self.delegate.onResize( width, height )
		self.viewWidth  = width
		self.viewHeight = height



##----------------------------------------------------------------##
class MOAIEditCanvas( MOAIEditCanvasBase ):
	def __init__( self, *args, **kwargs ):
		super( MOAIEditCanvas, self ).__init__( *args, **kwargs )
		# self.keyGrabbingCount = 0