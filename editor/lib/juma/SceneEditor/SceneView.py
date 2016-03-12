import os.path

from PySide  import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt
from PySide.QtGui import QFileDialog

from juma.core import signals, app
from juma.moai.MOAIEditCanvas import  MOAIEditCanvas



##----------------------------------------------------------------##
class SceneView( QtGui.QScrollArea ):
	def __init__( self, parent=None ):
		super(SceneView, self).__init__( parent )

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.canvas = SceneViewCanvas()
		self.setWidget(self.canvas)

		self.canvas.resize( 640, 480 )
		self.canvas.onMoaiReset()
		self.canvas.startUpdateTimer()

	def openSource(self):
		fileName, filt = QFileDialog.getOpenFileName(self, "Run Script", app.getProject().path or "~", "Lua source (*.lua )")
		if fileName:
			dir_path = os.path.dirname(fileName)
			file_path = os.path.basename(fileName)
			self.canvas.openFile( file_path, dir_path )


##----------------------------------------------------------------##
class SceneViewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( SceneViewCanvas, self ).__init__( *args, **kwargs )

	def openFile(self, file, path):
		runtime = self.runtime
		# runtime.resume()
		runtime.setWorkingDirectory( path )

		self.makeCurrent()
		runtime.runScript( file )
		# self.canvas.startRefreshTimer( self.activeFPS )
		# self.canvas.refreshTimer.start()