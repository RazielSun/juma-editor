import os.path

from PySide  import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from SceneEditor             	import SceneEditorModule



##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class SceneIntrospector( SceneEditorModule ):
	_name       = 'introspector'
	_dependency = [ 'qt', 'scene_editor' ]

	def __init__(self):
		super( SceneIntrospector, self ).__init__()

	def onLoad( self ):
		self.window = self.requestDockWindow('SceneIntrospector',
				title   = 'Introspector',
				dock    = 'left',
				minSize = (200,200)
		)

##----------------------------------------------------------------##

SceneIntrospector().register()