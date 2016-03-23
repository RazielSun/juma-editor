#!/usr/bin/env python

import os.path

from PySide  		import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas
from MainEditor             	import MainEditorModule
from SceneToolManager			import SceneToolButton, SceneTool

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
class SceneViewToolMoveObject( SceneViewTool ):
	name     = 'scene_view_move_object'
	shortcut = 'W'
	tool     = 'move_object'

##----------------------------------------------------------------##
class SceneViewToolRotateObject( SceneViewTool ):
	name     = 'scene_view_rotate_object'
	shortcut = 'E'
	tool     = 'rotate_object'

##----------------------------------------------------------------##
class SceneViewToolScaleObject( SceneViewTool ):
	name     = 'scene_view_scale_object'
	shortcut = 'R'
	tool     = 'scale_object'

##----------------------------------------------------------------##
class SceneView( MainEditorModule ):
	_name       = 'scene_view'
	_dependency = [ 'main_editor', 'graph_editor' ]

	def __init__(self):
		super( SceneView, self ).__init__()

	def onLoad( self ):
		self.window = self.requestDocumentWindow(
				title = 'new.layout'
			)

		self.tool = self.addToolBar( 'scene_view_config', self.window.addToolBar() )

		self.canvas = self.window.addWidget(
				SceneViewCanvas()
			)
		self.canvas.loadScript( _getModulePath('SceneView.lua') )

		self.findMenu( 'main/window' ).addChild([
            dict( name = 'scene_show', label = 'Scene View' ),
        ], self )

		self.window.show()

		# SIGNALS
		signals.connect( 'selection.changed', self.onSelectionChanged )
		signals.connect( 'scene.open',        self.onSceneOpen        )

		##----------------------------------------------------------------##
		self.mainToolBar = self.addToolBar( 'scene_view_tools', 
			self.getMainWindow().requestToolBar( 'view_tools' )
			)

		self.addTool(	'scene_view_tools/tool_drag_camera',
			widget = SceneToolButton( 'scene_view_drag_camera',
				icon = 'tools/moustache',
				label = 'Drag camera'
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

##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_show':
			self.window.show()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		self.canvas.safeCallMethod( 'scene', 'onSelectionChanged', selection )

	def changeEditTool( self, name ):
		self.canvas.makeCurrent()
		self.canvas.safeCallMethod( 'scene', 'changeEditTool', name )

	def onSceneOpen( self, title ):
		self.canvas.makeCurrent()
		self.window.setWindowTitle( title )

##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )