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

		# SIGNALS

		signals.connect( 'selection.changed', self.onSelectionChanged )

	def onSelectionChanged( self, selection, key ):
		if key != 'scene': return
		print("SceneIntrospector onSelectionChanged")
		# if not self.activeInstance: return
		# target = None
		# if isinstance( selection, list ):
		# 	target = selection
		# elif isinstance( selection, tuple ):
		# 	(target) = selection
		# else:
		# 	target=selection
		# #first selection only?
		# self.activeInstance.setTarget(target)

##----------------------------------------------------------------##

SceneIntrospector().register()