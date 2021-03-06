from PySide import QtCore, QtGui, QtOpenGL
from PySide.QtCore import Qt

from juma.qt.controls.GLWidget import GLWidget

def convertKeyCode(k):
	if k>1000:
		return (k&0xff)+(255 - 0x55)
	else:
		return k

class MOAICanvasBase(GLWidget):
	def __init__( self, parentWidget = None, **option ):
		# option['vsync'] = option.get('vsync', False)
		super(MOAICanvasBase,self).__init__( parentWidget, **option )		
		self.inputDevice = None
		self.buttonCount = 0

	def setInputDevice(self, device):
		self.inputDevice = device

	def mousePressEvent(self, event):	
		inputDevice = self.inputDevice
		if not inputDevice:
			return

		button = event.button()		
		if self.buttonCount == 0:
			self.grabMouse()
		self.buttonCount += 1
		inputDevice.getSensor('pointer').enqueueEvent(event.x(), event.y())
		if   button == Qt.LeftButton:
			inputDevice.getSensor('mouseLeft').enqueueEvent(True)
		elif button == Qt.RightButton:
			inputDevice.getSensor('mouseRight').enqueueEvent(True)
		elif button == Qt.MiddleButton:
			inputDevice.getSensor('mouseMiddle').enqueueEvent(True)

	def mouseReleaseEvent(self, event):
		inputDevice=self.inputDevice
		if not inputDevice:
			return

		self.buttonCount -= 1
		if self.buttonCount == 0:
			self.releaseMouse()
		button = event.button()
		inputDevice.getSensor('pointer').enqueueEvent(event.x(), event.y())
		if   button == Qt.LeftButton:
			inputDevice.getSensor('mouseLeft').enqueueEvent(False)
		elif button == Qt.RightButton:
			inputDevice.getSensor('mouseRight').enqueueEvent(False)
		elif button == Qt.MiddleButton:
			inputDevice.getSensor('mouseMiddle').enqueueEvent(False)

	def mouseMoveEvent(self, event):
		inputDevice=self.inputDevice
		if not inputDevice:
			return

		inputDevice.getSensor('pointer').enqueueEvent(event.x(), event.y())

	def wheelEvent(self, event):
		pass

	def keyPressEvent(self, event):
		if event.isAutoRepeat(): return
		inputDevice=self.inputDevice
		if not inputDevice:
			return

		key=event.key()
		inputDevice.getSensor('keyboard').enqueueKeyEvent(convertKeyCode(key), True)

	def keyReleaseEvent(self, event):
		inputDevice=self.inputDevice
		if not inputDevice:
			return
		
		key=event.key()
		inputDevice.getSensor('keyboard').enqueueKeyEvent(convertKeyCode(key), False)

