from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class GLWidget(QtOpenGL.QGLWidget):
	sharedWidget = None

	@staticmethod
	def getSharedWidget():
		if not GLWidget.sharedWidget:
			fmt=QtOpenGL.QGLFormat()
			fmt.setRgba(True)
			fmt.setAlpha(True)
			fmt.setDepth(True)
			fmt.setDoubleBuffer(True)
			fmt.setSampleBuffers(True)
			fmt.setSwapInterval(0)
			QtOpenGL.QGLFormat.setDefaultFormat(fmt)
			
			hiddenWindow = QtOpenGL.QGLWidget( QtOpenGL.QGLContext(fmt) )
			GLWidget.sharedWidget = hiddenWindow
			hiddenWindow.makeCurrent()
	
		return GLWidget.sharedWidget

	def __init__( self, parent=None, **option ):
		fmt = QtOpenGL.QGLFormat()
		if option.get( 'vsync', True ):
			fmt.setSwapInterval( 1 )
		else:
			fmt.setSwapInterval( 0 )

		fmt.setSampleBuffers( option.get( 'sample_buffer', True ) )

		QtOpenGL.QGLWidget.__init__( self, fmt, parent, GLWidget.getSharedWidget() )		
		self.setAttribute( Qt.WA_NoSystemBackground, True )
		self.setAttribute( Qt.WA_OpaquePaintEvent, True )
		self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
		self.setFocusPolicy(QtCore.Qt.ClickFocus)
		self.setMouseTracking(True)

		self.glReady = False
		self.windowReady = False

		self.allowRefresh   = False
		self.pendingRefresh = False

		self.refreshTimer   = QtCore.QTimer(self)
		self.refreshTimer.setSingleShot( True )
		self.refreshTimer.timeout.connect( self.onRefreshTimer )

	def initializeGL(self):
		self.glReady = True
		glClearColor(0, 0, 0, 1)

	def startRefreshTimer( self, fps = 60 ):
		self.allowRefresh = True
		interval = 1000/fps
		self.refreshTimer.setInterval( interval )
		self.refreshTimer.start()

	def stopRefreshTimer(self):
		self.allowRefresh = False
		self.refreshTimer.stop()

	def forceUpdateGL(self):
		self.allowRefresh = True
		self.refreshTimer.stop()
		self.updateGL()

	def minimumSizeHint(self):
		return QtCore.QSize(50, 50)

	#auto render if has pending render
	def onRefreshTimer(self): 
		print("GLWidget refreshTick")
		if self.pendingRefresh:
			self.pendingRefresh = False
			self.allowRefresh = True
			self.updateGL()
		self.allowRefresh = True

	def paintGL( self ):
		if self.windowReady:		
			self.onDraw()
		elif self.glReady:
			glClear(GL_COLOR_BUFFER_BIT)

	# def updateGL( self ):
	# 	print("GLWidget updateGl")
	# 	if not self.allowRefresh:
	# 		self.pendingRefresh = True
	# 		return
	# 	self.allowRefresh = False
	# 	self.refreshTimer.start()
	# 	super( GLWidget, self ).updateGL()

	def onDraw(self):
		pass



##----------------------------------------------------------------##
class CommonGLWidget(QtOpenGL.QGLWidget):
	def __init__( self, parent=None, **option ):
		fmt = QtOpenGL.QGLFormat()
		fmt.setRgba(True)
		fmt.setAlpha(True)
		fmt.setDepth(True)
		fmt.setDoubleBuffer(False)
		if option.get( 'vsync', False ):
			fmt.setSwapInterval( 1 )
		else:
			fmt.setSwapInterval( 0 )
		QtOpenGL.QGLWidget.__init__( self, fmt, parent, GLWidget.getSharedWidget() )		
		self.setFocusPolicy( QtCore.Qt.WheelFocus )