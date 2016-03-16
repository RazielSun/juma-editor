import os.path

from PySide  import QtCore, QtGui, QtOpenGL

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import  MOAIEditCanvas

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class LayoutView( QtGui.QScrollArea ):
	def __init__( self, parent=None ):
		super(LayoutView, self).__init__( parent )

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.canvas = LayoutViewCanvas( context_prefix = 'layout_edit' )
		self.setWidget( self.canvas )
		self.canvas.resize(400, 400)

		self.canvas.loadScript( _getModulePath('LayoutView.lua') )



##----------------------------------------------------------------##
class LayoutViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( LayoutViewCanvas, self ).__init__( *args, **kwargs )