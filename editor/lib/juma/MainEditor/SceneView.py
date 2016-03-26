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
class SceneViewToolDragCamera( SceneViewTool ):
	name     = 'scene_view_drag_camera'
	shortcut = 'Q'
	tool     = 'drag_camera'

##----------------------------------------------------------------##
class SceneViewToolSelectObject( SceneViewTool ):
	name     = 'scene_view_select_object'
	shortcut = 'W'
	tool     = 'select_object'

##----------------------------------------------------------------##
class SceneViewToolMoveObject( SceneViewTool ):
	name     = 'scene_view_move_object'
	shortcut = 'E'
	tool     = 'move_object'

##----------------------------------------------------------------##
class SceneViewToolRotateObject( SceneViewTool ):
	name     = 'scene_view_rotate_object'
	shortcut = 'R'
	tool     = 'rotate_object'

##----------------------------------------------------------------##
class SceneViewToolScaleObject( SceneViewTool ):
	name     = 'scene_view_scale_object'
	shortcut = 'T'
	tool     = 'scale_object'

##----------------------------------------------------------------##
class SceneView( MainEditorModule ):
	_name       = 'scene_view'
	_dependency = [ 'main_editor', 'graph_editor' ]

	def __init__(self):
		super( SceneView, self ).__init__()

	def onLoad( self ):
		self.window = self.requestDocumentWindow( title = 'new.layout' )

		self.sizeWidget = ToolSizeWidget( None )
		self.sizeWidget.valuesChanged.connect( self.onFrameResize )
		self.sizeWidget.owner = self

		self.coordWidget = ToolCoordWidget( None )
		self.coordWidget.gotoSignal.connect( self.goToPoint )
		self.coordWidget.owner = self

		self.tool = self.addToolBar( 'scene_view_config', self.window.addToolBar() )
		self.addTool( 'scene_view_config/grid_view', label = 'Grid', icon = 'grid' )
		self.addTool( 'scene_view_config/size_background', widget = self.sizeWidget )
		self.addTool( 'scene_view_config/zoom_out', label = 'Zoom Out', icon = 'glass_remove' )
		self.addTool( 'scene_view_config/zoom_normal', label = 'Zoom Normal', icon = 'glass' )
		self.addTool( 'scene_view_config/zoom_in', label = 'Zoom In', icon = 'glass_add' )
		self.addTool( 'scene_view_config/goto_point', widget = self.coordWidget )

		self.canvas = self.window.addWidget( SceneViewCanvas() )
		self.canvas.loadScript( _getModulePath('SceneView.lua') )

		self.findMenu( 'main/window' ).addChild([
            dict( name = 'scene_show', label = 'Scene View' ),
        ], self )

		##----------------------------------------------------------------##
		self.mainToolBar = self.addToolBar( 'scene_view_tools', 
			self.getMainWindow().requestToolBar( 'view_tools' )
			)

		self.addTool(	'scene_view_tools/tool_drag_camera',
			widget = SceneToolButton( 'scene_view_drag_camera',
				icon = 'tools/view',
				label = 'Drag camera'
				)
			)

		self.addTool(	'scene_view_tools/tool_select_object',
			widget = SceneToolButton( 'scene_view_select_object',
				icon = 'tools/dashed',
				label = 'Select object'
				)
			)

		self.addTool(	'scene_view_tools/tool_move_object',
			widget = SceneToolButton( 'scene_view_move_object',
				icon = 'tools/arrows',
				label = 'Move object'
				)
			)

		self.addTool(	'scene_view_tools/tool_rotate_object',
			widget = SceneToolButton( 'scene_view_rotate_object',
				icon = 'tools/rotate',
				label = 'Rotate object'
				)
			)

		self.addTool(	'scene_view_tools/tool_scale_object',
			widget = SceneToolButton( 'scene_view_scale_object',
				icon = 'tools/resize',
				label = 'Scale object'
				)
			)

		# SIGNALS
		signals.connect( 'selection.changed', self.onSelectionChanged )
		signals.connect( 'scene.open',        self.onSceneOpen        )

		#
		self.onZoom()
		self.window.show()

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

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		self.canvas.safeCallMethod( 'scene', 'onSelectionChanged', selection )

	def changeEditTool( self, name ):
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'scene', 'changeEditTool', name )

	def onSceneOpen( self, title ):
		self.canvas.makeCurrent()
		self.window.setWindowTitle( title )

	def onFrameResize( self, width, height ):
		self.canvas.safeCallMethod( 'scene', 'resizeFrame', width, height )

	def onZoom( self, zoom='normal' ):
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
		self.canvas.safeCallMethod( 'scene', 'goToPos', x, y )

##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )