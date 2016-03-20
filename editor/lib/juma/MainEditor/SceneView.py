#!/usr/bin/env python

import os.path

from PySide  		import QtCore, QtGui, QtOpenGL
from PySide.QtGui 	import QFileDialog

from juma.core 					import signals, app
from juma.core.layout 			import _saveLayoutToFile
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
				title = 'Scene'
			)

		self.tool = self.addToolBar( 'scene_view_config', self.window.addToolBar() )

		self.canvas = self.window.addWidget(
				SceneViewCanvas()
			)
		self.canvas.loadScript( _getModulePath('SceneView.lua') )

		self.findMenu( 'main/scene' ).addChild([
            dict( name = 'scene_show', label = 'Show Scene' ),
            dict( name = 'scene_open', label = 'Open Scene' ),
            dict( name = 'scene_save', label = 'Save Scene' ),
        ], self )

		self.window.show()

		# SIGNALS

		signals.connect( 'selection.changed', self.onSelectionChanged )

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

	def openScene(self): #(parent, caption = "Open file", directory = None, filter = None):
		fileName, filt = QFileDialog.getOpenFileName(self.getMainWindow(), "Open Scene", self.getProject().path or "~", "Layout file (*.layout )")
		# fileName, filt = QtGui.QFileDialog.getOpenFileName(parent, caption, directory, filter)
		print(" openScene fileName, filt", fileName, filt)
		# return fileName

	def saveScene(self):
		fileName, filt = QFileDialog.getSaveFileName(self.getMainWindow(), "Save Scene", self.getProject().path or "~", "Layout file (*.layout )")
		data = self.canvas.safeCallMethod( 'scene', 'save' )
		_saveLayoutToFile( fileName, data )

##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_show':
			self.window.show()

		elif name == 'scene_open':
			self.openScene()

		elif name == 'scene_save':
			self.saveScene()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		# self.canvas.safeCallMethod( 'view', 'onSelectionChanged', selection )

	def changeEditTool( self, name ):
		self.canvas.makeCurrent()
		print("SceneView changeEditTool", name)
		# self.canvas.safeCallMethod( 'view', 'changeEditTool', name )



##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )