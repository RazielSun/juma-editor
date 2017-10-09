#!/usr/bin/env python

from PySide import QtGui, QtCore
from PySide.QtCore import Qt, QEventLoop, QEvent, QObject

from juma.core import *
from juma.core.ModelManager import *

from juma.qt.helpers    import addWidgetWithLayout, restrainWidgetToScreen
from juma.qt.IconCache  import getIcon

from ui.array_view_container_ui			import Ui_ArrayViewContainer as ArrayViewContainer

##----------------------------------------------------------------##
def getModulePath( path ):
	import os.path
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class ArrayLineView( QtGui.QLineEdit ):
	def __init__(self, *args ):
		super( ArrayLineView, self ).__init__( *args )

##----------------------------------------------------------------##
class ArrayViewWidget( QtGui.QWidget ):
	def __init__(self, *args ):
		super( ArrayViewWidget, self ).__init__( *args )
		self.views = []
		self.counts = 0

		self.setWindowFlags( Qt.Popup )
		self.ui = ui = ArrayViewContainer()
		ui.setupUi( self )

		ui.bodyLayout.setAlignment(QtCore.Qt.AlignTop)

		intValidator = QtGui.QIntValidator()
		ui.totalEdit.setText( str(self.counts) )
		ui.totalEdit.setValidator( intValidator )
		ui.totalEdit.returnPressed.connect( self.onTotalEditPressed )

		ui.totalBtn.setText( 'Save' )
		ui.totalBtn.clicked.connect( self.onTotalButtonClick )
		
		self.setMinimumSize( 300, 200  )

	def body( self ):
		return self.ui.bodyLayout

	def hideAll( self ):
		for view in self.views:
			view.hide()

	def setup( self, typeId, data ):
		self.hideAll()
		total = 0
		if data:
			total = len(data)
			self.createLines( total )
			i = 0
			for d in data:
				self.fill( i, d )
				i += 1
		self.ui.totalEdit.setText(str(total))

	def createLines( self, total ):
		self.hideAll()
		count = len(self.views)
		self.counts = total

		for i in range(0, total):
			view = None
			if count > i:
				view = self.views[i]
				view.show()
			else:
				view = self.getLine()
				self.body().addWidget( view )
				self.views.append( view )
		height = total * 28 + 40
		self.resize( 350, height )

	def fill( self, index, value ):
		view = self.views[index]
		view.setText(str(value))

	def getLine( self ):
		return ArrayLineView( self )

	##----------------------------------------------------------------##
	def collect( self ):
		arr = []
		for i in range(0, self.counts):
			view = self.views[i]
			txt = view.text()
			arr.append( txt )
		return arr

	##----------------------------------------------------------------##
	def onTotalEditPressed( self ):
		total = int(self.ui.totalEdit.text())
		self.createLines( total )

	def onTotalButtonClick( self ):
		self.module.saveData()

##----------------------------------------------------------------##
## Array View
##----------------------------------------------------------------##
class ArrayView( EditorModule ):
	_name = 'array_view'
	_dependency = [ 'qt' ]

	def __init__( self ):
		self.onSave = None

	def onLoad( self ):
		self.window = ArrayViewWidget( None )
		self.window.module = self

	def request( self, **option ):
		pos        = option.get( 'pos', QtGui.QCursor.pos() )
		typeId     = option.get( 'type', None )
		context    = option.get( 'context', None )
		initial    = option.get( 'initial', None )

		self.onSave = option.get('on_save', None)

		self.window.move( pos )
		restrainWidgetToScreen( self.window )

		self.window.setup( typeId, initial )

		self.window.show()
		self.window.raise_()
		self.window.setFocus()

	def saveData( self ):
		if self.onSave:
			self.onSave( self.window.collect() )
		self.window.hide()

##----------------------------------------------------------------##

arrayView = ArrayView()
arrayView.register()

##----------------------------------------------------------------##

def requestArrayView( **option ):
	return arrayView.request( **option )
