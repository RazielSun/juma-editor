import os.path

from PySide  import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import  MOAIEditCanvas
from SceneEditor             	import SceneEditorModule



##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class SceneView( SceneEditorModule ):
	_name       = 'scene_view'
	_dependency = [ 'scene_editor', 'scenegraph_editor' ]

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
        ], self )

		self.window.show()

		# SIGNALS

		signals.connect( 'selection.changed', self.onSelectionChanged )

##----------------------------------------------------------------##
	def onMenu( self, tool ):
		name = tool.name
		if name == 'scene_show':
			self.window.show()

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		# self.canvas.safeCallMethod( 'view', 'onSelectionChanged', selection )

##----------------------------------------------------------------##

SceneView().register()

##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )