import os.path
import time
import logging

from PySide                   import QtCore, QtGui, QtOpenGL
from PySide.QtCore            import Qt

from juma.core                import signals, app

# from juma.moai.MOAIRuntime    import getAKU
from juma.moai.MOAICanvasBase import MOAICanvasBase
from juma.qt.controls.GLWidget import GLWidget
# from gii.moai.MOAIEditCanvas import MOAIEditCanvas

from SceneEditor             import SceneEditorModule
# import ExternRun

##----------------------------------------------------------------##
class GamePreview( SceneEditorModule ):
	"""docstring for GamePreview"""
	_name = 'game_preview'
	_dependency = [ 'qt', 'moai', 'scene_editor' ]

	def __init__(self):
		super(GamePreview, self).__init__()
		self.runtime 		= None
		self.started 		= False
		self.paused         = False
		self.waitActivate   = False
		self.viewWidth      = 0
		self.viewHeight     = 0
		self.pendingScript  = None
		self.activeFPS      = 60
		self.nonActiveFPS   = 15

	def getRuntime(self):
		if not self.runtime:
			self.runtime = self.affirmModule('moai')
		return self.runtime

	# def tryResizeContainer(self, w,h):
	# 	return True	#TODO:client area	

	# def setOrientationPortrait( self ):
	# 	if self.window.isFloating():
	# 		pass #TODO
	# 	getAKU().setOrientationPortrait()

	# def setOrientationLandscape( self ):
	# 	if self.window.isFloating():
	# 		pass #TODO
	# 	getAKU().setOrientationLandscape()

	# def onOpenWindow(self, title, w,h):
	# 	logging.info('opening MOAI window: %s @ (%d,%d)' % ( str(title), w, h ) )
	# 	#no argument accepted here, just use full window
	# 	# self.getRuntime().initGLContext()
	# 	from gii.qt.controls.GLWidget import GLWidget
	# 	GLWidget.getSharedWidget().makeCurrent()

	# 	self.originalSize = (w,h)
	# 	self.tryResizeContainer( *self.originalSize )

	# 	size=self.canvas.size()
	# 	w,h = size.width(),size.height()

	# 	getAKU().setScreenSize(w,h)
	# 	getAKU().setViewSize(w,h)


	def onLoad(self):
		self.paused = None

		self.window = self.requestDockWindow(
			'GamePreview',
			title = 'Game Preview',
			dock  = 'right'
			)

		# self.window.hideTitleBar()
		self.window.setFocusPolicy(Qt.StrongFocus)

		toolbar = self.window.addToolBar()
		self.toolbar = self.addToolBar( 'game_preview', toolbar )
		
		self.scrollArea = QtGui.QScrollArea( None )
		self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
		self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
		self.window.addWidget( self.scrollArea )

		self.canvas = GamePreviewCanvas()
		self.viewWidth = 320
		self.viewHeight = 480
		self.canvas.resize(self.viewWidth, self.viewHeight)
		self.scrollArea.setWidget( self.canvas )
		self.canvas.startRefreshTimer( self.nonActiveFPS )
		self.canvas.module = self

		self.updateTimer = None
		
	# 	signals.connect( 'app.activate',   self.onAppActivate )
	# 	signals.connect( 'app.deactivate', self.onAppDeactivate )
		
	# 	signals.connect( 'debug.enter',    self.onDebugEnter )
	# 	signals.connect( 'debug.exit',     self.onDebugExit )
	# 	signals.connect( 'debug.stop',     self.onDebugStop )
		
		signals.connect( 'moai.reset',     		self.onMoaiReset )
		signals.connect( 'moai.open_window', 	self.openWindow )
		# signals.connect('moai.set_sim_step', self.setSimStep)
		
		self.menu = self.findMenu( 'main/preview' )

		self.menu.addChild([
				{'name':'run_game',   'label':'Run'}, #, 'shortcut':'meta+]' 
				{'name':'pause_game', 'label':'Pause' }, #,  'shortcut':'meta+shit+]'
				{'name':'stop_game',  'label':'Stop'}, #,   'shortcut':'meta+['
			], self)

		##----------------------------------------------------------------##
		self.previewToolBar = self.addToolBar( 'game_preview_tools', 
			self.getMainWindow().requestToolBar( 'preview_tools' )
			)

		self.addTool('game_preview_tools/run_game', label = 'Run',
			menu_link = 'main/preview/run_game', icon = 'tools/play')

		self.addTool('game_preview_tools/pause_game', label = 'Pause',
			menu_link = 'main/preview/pause_game', icon = 'tools/pause',)
		
		self.addTool('game_preview_tools/stop_game', label = 'Stop',
			menu_link = 'main/preview/stop_game', icon = 'tools/stop',)

		self.enableMenu( 'main/preview/pause_game',  False )
		self.enableMenu( 'main/preview/stop_game',   False )

	def onStop( self ):
		if self.updateTimer:
			self.updateTimer.stop()

	def show( self ):
		self.window.show()

	def hide( self ):
		self.window.hide()

	def refresh( self ):
		self.canvas.updateGL()

	# Update AKU
	def makeCurrent(self):
		# GLWidget.getSharedWidget().makeCurrent()
		self.getRuntime().changeRenderContext( 'game', self.viewWidth, self.viewHeight )

	def updateView(self):
		if self.paused: return
		self.makeCurrent()
		if self.getRuntime().updateAKU():
			self.canvas.forceUpdateGL()

	def resizeView(self, w, h):
		self.viewWidth  = w
		self.viewHeight = h
		runtime = self.getRuntime()
		runtime.setScreenSize( w, h )
		runtime.setViewSize( w, h )

	def renderView(self):
		runtime = self.getRuntime()
		# runtime.setViewSize( self.viewWidth, self.viewHeight )
		self.makeCurrent()
		runtime.renderAKU()

	def onMoaiReset( self ):
		runtime = self.getRuntime()
		runtime.createRenderContext( 'game' )
		runtime.setLuaEnvResolution( self.viewWidth, self.viewHeight )
		runtime.runGame()

	def openWindow(self, title, width, height):
		# self.canvas.resize(width, height)
		self.resizeView( self.viewWidth, self.viewHeight )
	
	# def onDebugEnter(self):
	# 	self.paused = True
	# 	self.getRuntime().pause()
	# 	self.window.setFocusPolicy(Qt.NoFocus)

	# def onDebugExit(self, cmd=None):
	# 	self.paused=False
	# 	self.getRuntime().resume()
	# 	self.window.setFocusPolicy(Qt.StrongFocus)
	# 	if self.pendingScript:
	# 		script = self.pendingScript
	# 		self.pendingScript=False
	# 		self.restartScript(script)
	# 	self.setFocus()
		
	# def onDebugStop(self):
	# 	self.paused=True

	# def onAppActivate(self):
	# 	if self.waitActivate:
	# 		self.waitActivate=False
	# 		self.getRuntime().resume()

	# def onAppDeactivate(self):
	# 	if self.getConfig('pause_on_leave',False):
	# 		self.waitActivate=True
	# 		self.getRuntime().pause()

	def onSetFocus(self):
		self.window.show()
		self.window.raise_()
		self.window.setFocus()
		self.canvas.setFocus()
		self.canvas.activateWindow()
		self.setActiveWindow( self.window )

	def runPreview(self):
		if self.paused == False: return

		self.makeCurrent()

		runtime = self.getRuntime()
		self.canvas.setInputDevice( runtime.getInputDevice('device') )

		self.getApp().setMinimalMainLoopBudget()

		# self.canvas.startRefreshTimer( self.activeFPS )
		# self.canvas.refreshTimer.start()
		# 	self.canvas.interceptShortcut = True

		self.enableMenu( 'main/preview/pause_game', True )
		self.enableMenu( 'main/preview/stop_game',  True )
		self.enableMenu( 'main/preview/run_game', 	False )

		if self.paused:
			self.updateTimer.start()
			signals.emitNow( 'preview.resume' )
		elif self.paused is None:
			signals.emitNow( 'preview.start' )
			signals.emitNow( 'preview.resume' )
			self.updateTimer = self.window.startTimer( runtime.simStep, self.updateView )

		self.window.setWindowTitle( 'Game Preview [ RUNNING ]')
		
		self.paused = False
		runtime.resume()
		self.setFocus()

	def stopPreview(self):
		if self.paused is None: return

		self.canvas.setInputDevice( None )
		# 	self.canvas.interceptShortcut = False

		self.getApp().resetMainLoopBudget()

		signals.emitNow( 'preview.stop' )
		self.updateTimer.stop()

		self.enableMenu( 'main/preview/stop_game',  False )
		self.enableMenu( 'main/preview/pause_game', False )
		self.enableMenu( 'main/preview/run_game', 	True )

		self.window.setWindowTitle( 'Game Preview' )

		self.updateTimer = None
		self.paused = None
		# 	self.canvas.startRefreshTimer( self.nonActiveFPS )

	def pausePreview(self):
		if self.paused: return
		
		self.canvas.setInputDevice( None )

		self.getApp().resetMainLoopBudget()

		signals.emitNow( 'preview.pause' )

		self.enableMenu( 'main/preview/run_game', 	True )
		self.enableMenu( 'main/preview/pause_game',	False )

		self.window.setWindowTitle( 'Game Preview[ Paused ]')

		runtime = self.getRuntime()
		runtime.pause()
		self.paused = True
		# 	self.canvas.startRefreshTimer( self.nonActiveFPS )

##----------------------------------------------------------------##
	def onMenu(self, node):
		name = node.name

		if name == 'run_game':
			self.runPreview()

		elif name == 'pause_game':
			self.pausePreview()

		elif name == 'stop_game':
			self.stopPreview()

		# if name == 'open_scene':
		# 	self.openProject()
	# 	if name=='size_double':
	# 		if self.originalSize:
	# 			w,h=self.originalSize
	# 			self.tryResizeContainer(w*2,h*2)

	# 	elif name=='size_original':
	# 		if self.originalSize:
	# 			w,h=self.originalSize
	# 			self.tryResizeContainer(w,h)

	# 	elif name=='pause_on_leave':
	# 		self.setConfig( 'pause_on_leave', node.getValue())

	# 	elif name=='reset_moai':
	# 		#TODO: dont simply reset in debug
	# 		# self.restartScript( self.runningScript )
	# 		self.getRuntime().reset()

	# 	elif name=='orient_portrait':
	# 		self.setOrientationPortrait()

	# 	elif name=='orient_landscape':
	# 		self.setOrientationLandscape()

	# 	elif name == 'start_game':
	# 		self.startPreview()

	# 	elif name == 'stop_game':
	# 		self.stopPreview()

	# 	elif name == 'pause_game':
	# 		self.pausePreview()

	# 	elif name == 'start_external_scene':
	# 		self.runSceneExternal()
			
	# 	elif name == 'start_external_game':
	# 		self.runGameExternal()

	# def onTool( self, tool ):
	# 	name = tool.name
	# 	if name == 'switch_screen_profile':
	# 		pass
			
	# 	elif name == 'run_external':
	# 		self.runSceneExternal()

	# 	elif name == 'run_game_external':
	# 		self.runGameExternal()

##----------------------------------------------------------------##
class GamePreviewCanvas(MOAICanvasBase):
	def __init__( self, *args, **kwargs ):
		super( GamePreviewCanvas, self ).__init__( *args, **kwargs )
		self.interceptShortcut = False
		self.installEventFilter( self )

	def eventFilter( self, obj, ev ):
		if not self.interceptShortcut: return False
		if obj == self:
			etype = ev.type()
			if etype == QtCore.QEvent.ShortcutOverride:
				self.keyPressEvent( ev )
				ev.accept()
				return True
		return False

	def resizeGL(self, width, height):
		self.module.resizeView(width, height)
		MOAICanvasBase.resizeGL(self, width, height)

	def onDraw(self):
		self.module.renderView()

##----------------------------------------------------------------##

GamePreview().register()
