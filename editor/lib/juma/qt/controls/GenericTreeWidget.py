
from PySide                   import QtCore, QtGui, QtOpenGL



##----------------------------------------------------------------##
class GenericTreeWidget( QtGui.QTreeWidget ):
	def __init__( self, *args, **option ):
		super(GenericTreeWidget, self).__init__(*args)