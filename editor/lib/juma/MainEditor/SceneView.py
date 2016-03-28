#!/usr/bin/env python

import os.path

from PySide  		import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas
from MainEditor             	import MainEditorModule
from SceneToolManager			import SceneToolButton, SceneTool
from MainEditorHelpers         	import ToolSizeWidget, ToolCoordWidget

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

	def onLoad( self ):
		self.window = self.requestDocumentWindow( title = 'new.layout' )

		self.sizeWidget = ToolSizeWidget( None )
		self.sizeWidget.valuesChanged.connect( self.onFrameResize )
		self.sizeWidget.owner = self

		self.coordWidget = ToolCoordWidget( None )
		self.coordWidget.gotoSignal.connect( self.goToPoint )
		self.coordWidget.owner = self

		self.tool = self.addToolBar( 'scene_view_config', self.window.addToolBar() )
		# self.addTool( 'scene_view_config/grid_view', label = 'Grid', icon = 'grid' )
		# self.addTool( 'scene_view_config/size_background', widget = self.sizeWidget )
		# self.addTool( 'scene_view_config/zoom_out', label = 'Zoom Out', icon = 'glass_remove' )
		# self.addTool( 'scene_view_config/zoom_normal', label = 'Zoom Normal', icon = 'glass' )
		# self.addTool( 'scene_view_config/zoom_in', label = 'Zoom In', icon = 'glass_add' )
		# self.addTool( 'scene_view_config/goto_point', widget = self.coordWidget )

		self.canvas = self.window.addWidget( SceneViewCanvas() )
		self.canvas.loadScript( _getModulePath('SceneView.lua') )

		self.findMenu( 'main/window' ).addChild([
            dict( name = 'scene_show', label = 'Scene View' ),
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
		signals.connect( 'selection.changed', self.onSelectionChanged )

		signals.connect( 'scene.open',        self.onSceneOpen        )

	def onStart( self ):
		self.scheduleUpdate()
		self.updateTimer = self.window.startTimer( 0.016, self.onUpdateTimer )
		self.updateTimer.stop()
		# FIXME
		scene = self.canvas.safeCall( 'createScene' )
		signals.emitNow( 'scene.change', scene )
		self.window.show()
		# ----

	def scheduleUpdate( self ):
		self.updatePending = True

	def forceUpdate( self ):
		self.scheduleUpdate()
		self.onUpdateTimer()

##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_show':
			self.window.show()

	def onTool( self, tool ):
		name = tool.name
		if name == 'zoom_out':
			self.onZoom( 'out' )
		elif name == 'zoom_normal':
			self.onZoom( 'normal' )
		elif name == 'zoom_in':
			self.onZoom( 'in' )

		elif name == 'grid_view':
			pass

	def onUpdateTimer( self ):
		if self.updatePending == True:
			self.updatePending = False
			self.canvas.updateCanvas( no_sim = self.previewing, forced = True )
			if not self.previewing:
				self.getModule( 'game_preview' ).refresh()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'view', 'onSelectionChanged', selection )

	def changeEditTool( self, name ):
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'view', 'changeEditTool', name )

	def onSceneOpen( self, scene ):
		# self.window.setWindowTitle( title )
		self.canvas.makeCurrent()
		self.canvas.safeCall( 'onSceneOpen', scene )
		self.setFocus()
		self.changeEditTool( 'translation' )
		self.updateTimer.start()
		self.forceUpdate()
		self.scheduleUpdate()

	def onFrameResize( self, width, height ):
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'scene', 'resizeFrame', width, height )

	def onZoom( self, zoom='normal' ):
		self.canvas.makeCurrent()
		maxed = self.canvas.safeCallMethod( 'scene', 'cameraZoom', zoom )
		if zoom:
			zoomN = True
			zoomI = True
			zoomO = True
			if zoom == 'normal':
				zoomN = False
			elif zoom == 'in':
				zoomI = not maxed
			elif zoom == 'out':
				zoomO = not maxed
			self.enableTool('scene_view_config/zoom_normal', zoomN)
			self.enableTool('scene_view_config/zoom_in', zoomI)
			self.enableTool('scene_view_config/zoom_out', zoomO)

	def goToPoint( self, x, y ):
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'scene', 'goToPos', x, y )

##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )
