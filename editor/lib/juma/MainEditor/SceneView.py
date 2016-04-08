#!/usr/bin/env python

import os.path

from PySide  		import QtCore, QtGui, QtOpenGL
from PySide.QtGui 	import QFileDialog

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas
from MainEditor             	import MainEditorModule, getSceneSelectionManager
from SceneToolManager			import SceneToolButton, SceneTool
from MainEditorHelpers         	import ToolSizeWidget, ToolCoordWidget
from juma.SearchView 			import requestSearchView

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class SceneViewTool( SceneTool ):
	def getSceneViewToolId( self ):
		toolId = getattr( self.__class__, 'tool' )
		if not toolId:
			raise Exception( 'no scene view tool Id specified' )
		return toolId

	def onStart( self, **context ):
		canvasToolId = self.getSceneViewToolId()
		app.getModule( 'scene_view' ).changeEditTool( canvasToolId )

##----------------------------------------------------------------##
class SceneViewToolSelectObject( SceneViewTool ):
	name     = 'scene_view_selection'
	shortcut = 'Q'
	tool     = 'selection'

##----------------------------------------------------------------##
class SceneViewToolMoveObject( SceneViewTool ):
	name     = 'scene_view_translation'
	shortcut = 'W'
	tool     = 'translation'

##----------------------------------------------------------------##
class SceneViewToolRotateObject( SceneViewTool ):
	name     = 'scene_view_rotation'
	shortcut = 'E'
	tool     = 'rotation'

##----------------------------------------------------------------##
class SceneViewToolScaleObject( SceneViewTool ):
	name     = 'scene_view_scale'
	shortcut = 'R'
	tool     = 'scale'

##----------------------------------------------------------------##
class SceneView( MainEditorModule ):
	_name       = 'scene_view'
	_dependency = [ 'main_editor', 'graph_editor' ]

	def __init__(self):
		super( SceneView, self ).__init__()
		self.updateTimer        = None
		self.updatePending      = False
		self.previewing         = False
		self.previewUpdateTimer = False

		self.windows = []
		self.filePaths = []
		self.fileTypes = []
		self.loaded = []

	def onLoad( self ):
		window = self.getMainWindow()
		window.tabChanged.connect( self.onTabChanged )
		window.tabRemoved.connect( self.onTabRemoved )
		
		self.findMenu( 'main/scene' ).addChild([
            dict( name = 'new_scene', label = 'New Scene' ),
            dict( name = 'open_scene', label = 'Open Scene' ),
            dict( name = 'open_scene_as', label = 'Open Scene As...' ),
            dict( name = 'save_scene', label = 'Save Scene' ),
            dict( name = 'save_scene_as', label = 'Save Scene As...' ),
        ], self )

		self.findMenu( 'main/entity' ).addChild([
			dict( name = 'move_to_selected', label = 'Camera Move To Selected', shortcut = 'F' )
		], self )

		self.findMenu( 'main/ui' ).addChild([
			dict( name = 'new_ui', label = 'New UI' ),
			dict( name = 'open_ui', label = 'Open UI', shortcut = 'ctrl+O' ),
			dict( name = 'open_ui_as', label = 'Open UI As...', shortcut = 'ctrl+shift+O' ),
			dict( name = 'save_ui', label = 'Save UI', shortcut = 'ctrl+S' ),
			dict( name = 'save_ui_as', label = 'Save UI As...', shortcut = 'ctrl+shift+S' ),
		], self )

		##----------------------------------------------------------------##
		self.mainToolBar = self.addToolBar( 'scene_view_tools', 
			self.getMainWindow().requestToolBar( 'view_tools' )
			)

		self.addTool(	'scene_view_tools/tool_selection',
			widget = SceneToolButton( 'scene_view_selection',
				icon = 'tools/dashed',
				label = 'Selection'
				)
			)

		self.addTool(	'scene_view_tools/tool_translation',
			widget = SceneToolButton( 'scene_view_translation',
				icon = 'tools/arrows',
				label = 'Move object'
				)
			)

		self.addTool(	'scene_view_tools/tool_rotation',
			widget = SceneToolButton( 'scene_view_rotation',
				icon = 'tools/rotate',
				label = 'Rotate object'
				)
			)

		self.addTool(	'scene_view_tools/tool_scale',
			widget = SceneToolButton( 'scene_view_scale',
				icon = 'tools/resize',
				label = 'Scale object'
				)
			)

		# SIGNALS
		signals.connect( 'entity.modified',   self.onEntityModified   )

		signals.connect( 'selection.changed', self.onSelectionChanged )

		signals.connect( 'scene.open',        self.onSceneOpen        )

		signals.connect( 'moai.ready',		  self.onMoaiReady	      )

	def onStart( self ):
		self.scheduleUpdate()
		self.updateTimer = self.startTimer( 0.016, self.onUpdateTimer )
		self.updateTimer.stop()

	def scheduleUpdate( self ):
		self.updatePending = True

	def forceUpdate( self ):
		self.scheduleUpdate()
		self.onUpdateTimer()

	def getTab( self ):
		mainWindow = self.getMainWindow()
		return mainWindow.centerTabWidget

	def getCurrentWindow( self ):
		mainWindow = self.getMainWindow()
		return mainWindow.centerTabWidget.currentWidget()

	def getCanvas( self ):
		window = self.getCurrentWindow()
		if window:
			return window.canvas
		return None

	def getWindowIndex( self, window ):
		index = -1
		for i,w in enumerate(self.windows):
			if w == window:
				index = i
				break
		return index

	def startTimer(self, step, trigger):
		assert(hasattr(trigger,'__call__'))
		interval = 1000 * step
		timer=QtCore.QTimer()
		timer.timeout.connect(trigger)
		timer.start(interval)
		return timer

	def newUI( self, path=None ):
		self.newDock( path, "ui" )

	def newScene( self, path=None ):
		self.newDock( path, "scene" )

	def newDock( self, path=None, dtype="scene" ):
		title = 'new.{} *'.format( dtype )
		self.fileTypes.append(dtype)
		if path:
			title = os.path.basename( path )
			self.filePaths.append( path )
		else:
			self.filePaths.append( None )

		window = self.requestDocumentWindow( title = title )
		self.windows.append(window)

		window.tool = tool = self.addToolBar( 'scene_view_config', window.addToolBar() )
		window.canvas = canvas = window.addWidget( SceneViewCanvas() )
		canvas.loadScript( _getModulePath('SceneView.lua') )
		self.loaded.append(True)

		self.addTool( 'scene_view_config/grid_view', label = 'Grid', icon = 'grid' )

		if dtype == "ui":
			window.framesize = framesize = ToolSizeWidget( None )
			framesize.valuesChanged.connect( self.onFrameResize )
			framesize.owner = self
			self.addTool( 'scene_view_config/canvas_frame', widget = framesize )

		# self.addTool( 'scene_view_config/zoom_out', label = 'Zoom Out', icon = 'glass_remove' )
		# self.addTool( 'scene_view_config/zoom_normal', label = 'Zoom Normal', icon = 'glass' )
		# self.addTool( 'scene_view_config/zoom_in', label = 'Zoom In', icon = 'glass_add' )
		# self.addTool( 'scene_view_config/goto_point', widget = self.coordWidget )

		# self.coordWidget = ToolCoordWidget( None )
		# self.coordWidget.gotoSignal.connect( self.goToPoint )
		# self.coordWidget.owner = self

		window.show()

		scene = canvas.safeCall( 'createScene', path, dtype )
		signals.emitNow( 'scene.change', scene )

	def openScene( self, stype="scene" ):
		requestSearchView( 
			context      = 'asset',
			type         = stype,
			multiple_selection = False,
			on_selection = self.onSceneSearchSelection,
			on_cancel    = self.onSceneSearchCancel,
			# on_search    = self.onSceneSearch,
			)

	def openSceneAs( self, stype="scene" ):
		filePath, filt = QFileDialog.getOpenFileName(self.getMainWindow(), "Open As", self.getProject().path or "~", "File (*.{})".format(stype))
		if filePath:
			self.newDock( filePath, stype )

	def saveScene( self, stype="scene" ):
		currentPath = None
		windowIndex = self.getWindowIndex( self.getCurrentWindow() )
		if windowIndex >= 0:
			currentPath = self.filePaths[windowIndex]
		if currentPath:
			self.saveSceneByPath( currentPath )
		else:
			self.saveSceneAs( stype )

	def saveSceneAs( self, stype="scene" ):
		filePath, filt = QFileDialog.getSaveFileName(self.getMainWindow(), "Save As", self.getProject().path or "~", "File (*.{})".format(stype))
		if filePath:
			self.saveSceneByPath( filePath )

	def saveSceneByPath( self, path ):
		canvas = self.getCanvas()
		success = canvas.safeCall( 'saveScene', path )

		window = self.getCurrentWindow()
		windowIndex = self.getWindowIndex( window )
		if windowIndex >= 0:
			self.filePaths[windowIndex] = path

		title = os.path.basename(path)
		tab = self.getTab()
		idx = tab.indexOf( window )
		if idx >= 0:
			tab.setTabText( idx, title )

	def recreateScene( self ):
		window = self.getCurrentWindow()
		index = self.getWindowIndex( window )
		if index >= 0:
			loaded = self.loaded[index]
			if not loaded:
				self.loaded[index] = True
				canvas = window.canvas
				scene = canvas.safeCall( 'createScene', self.filePaths[index], self.fileTypes[index] )
				signals.emitNow( 'scene.change', scene )

	def changeGridView( self ):
		canvas = self.getCanvas()
		if canvas:
			canvas.safeCallMethod( 'view', 'changeVisibleGrid' )

	def moveCameraToSelected( self ):
		canvas = self.getCanvas()
		if canvas:
			canvas.safeCallMethod( 'view', 'moveCameraToSelected' )

##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		
		if name == 'new_scene':
			self.newScene()
		elif name == 'open_scene':
			self.openScene()
		elif name == 'open_scene_as':
			self.openSceneAs()
		elif name == 'save_scene':
			self.saveScene()
		elif name == 'save_scene_as':
			self.saveSceneAs()

		elif name == 'new_ui':
			self.newUI()
		elif name == 'open_ui':
			self.openScene("ui")
		elif name == 'open_ui_as':
			self.openSceneAs("ui")
		elif name == 'save_ui':
			self.saveScene("ui")
		elif name == 'save_ui_as':
			self.saveSceneAs("ui")

		elif name == 'move_to_selected':
			self.moveCameraToSelected()

	def onTool( self, tool ):
		name = tool.name
		
		if name == 'grid_view':
			self.changeGridView()
		# if name == 'zoom_out':
		# 	self.onZoom( 'out' )
		# elif name == 'zoom_normal':
		# 	self.onZoom( 'normal' )
		# elif name == 'zoom_in':
		# 	self.onZoom( 'in' )

		# elif name == 'grid_view':
		# 	pass

	def onTabChanged( self, window ):
		getSceneSelectionManager().clearSelection()
		if window and window in self.windows:
			self.updateTimer.start()			
			scene = window.canvas.safeCall( 'getScene' )
			if scene:
				signals.emitNow( 'scene.change', scene )
			else:
				self.recreateScene()

	def onTabRemoved( self, window ):
		if window and window in self.windows:
			current = self.getCurrentWindow()
			if window == current:
				getSceneSelectionManager().clearSelection()
			index = self.getWindowIndex( window )
			if index >= 0:
				self.windows.pop(index)
				self.filePaths.pop(index)
				self.fileTypes.pop(index)
				self.loaded.pop(index)

	def onSceneSearchSelection( self, target ):
		if target:
			self.newDock( target.getNodePath(), target.getType() )

	def onSceneSearchCancel( self ):
		pass

	def onSceneSearch( self, typeId, context, option ):
		pass

	def onUpdateTimer( self ):
		if self.updatePending == True:
			self.updatePending = False
			canvas = self.getCanvas()
			if canvas:
				canvas.updateCanvas( no_sim = self.previewing, forced = True )
			if not self.previewing:
				self.getModule( 'game_preview' ).refresh()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		canvas = self.getCanvas()
		if canvas:
			canvas.makeCurrent()
			canvas.safeCallMethod( 'view', 'onSelectionChanged', selection )

	def changeEditTool( self, name ):
		canvas = self.getCanvas()
		if canvas:
			canvas.makeCurrent()
			canvas.safeCallMethod( 'view', 'changeEditTool', name )

	def onSceneOpen( self, scene ):
		canvas = self.getCanvas()
		if canvas:
			canvas.makeCurrent()
			created = canvas.safeCall( 'viewCreated' )
			if not created:
				canvas.safeCall( 'onSceneOpen', scene )
				self.changeEditTool( 'translation' )
			self.updateTimer.start()
			self.forceUpdate()
			self.scheduleUpdate()
			self.setFocus()

		window = self.getCurrentWindow()
		index = self.getWindowIndex( window )
		if index >= 0:
			window.resize(self.getTab().size())

	def onEntityModified( self, entity, context=None ):
		canvas = self.getCanvas()
		if canvas:
			canvas.makeCurrent()
			self.forceUpdate()

	def onFrameResize( self, width, height ):
		canvas = self.getCanvas()
		if canvas:
			canvas.makeCurrent()
			canvas.safeCallMethod( 'view', 'resizeFrame', width, height )

	def onMoaiReady( self ):
		for i,l in enumerate(self.loaded):
			self.loaded[i] = False
		self.recreateScene()

	# def onZoom( self, zoom='normal' ):
	# 	self.canvas.makeCurrent()
	# 	maxed = self.canvas.safeCallMethod( 'scene', 'cameraZoom', zoom )
	# 	if zoom:
	# 		zoomN = True
	# 		zoomI = True
	# 		zoomO = True
	# 		if zoom == 'normal':
	# 			zoomN = False
	# 		elif zoom == 'in':
	# 			zoomI = not maxed
	# 		elif zoom == 'out':
	# 			zoomO = not maxed
	# 		self.enableTool('scene_view_config/zoom_normal', zoomN)
	# 		self.enableTool('scene_view_config/zoom_in', zoomI)
	# 		self.enableTool('scene_view_config/zoom_out', zoomO)

	# def goToPoint( self, x, y ):
	# 	self.canvas.makeCurrent()
	# 	self.canvas.safeCallMethod( 'scene', 'goToPos', x, y )

##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )
