#!/usr/bin/env python

from PySide import QtGui, QtCore
from PySide.QtCore import Qt, QEventLoop, QEvent, QObject

from juma.core import *
from juma.core.ModelManager import *

# from gii.qt.controls.GenericTreeWidget import GenericTreeWidget
# from gii.qt.helpers    import addWidgetWithLayout, restrainWidgetToScreen
# from gii.qt.IconCache  import getIcon

# from ui.object_container_ui 			import Ui_ObjectContainer

##----------------------------------------------------------------##
class SearchViewWidget( QtGui.QWidget ):
	def __init__(self, *args ):
		super( SearchViewWidget, self ).__init__( *args )
		# self.searchState = None

		# self.setWindowFlags( Qt.Popup )
		# self.ui = SearchViewForm()
		# self.ui.setupUi( self )

		# self.ui = Ui_ObjectContainer()
		# self.ui.setupUi( self )

##----------------------------------------------------------------##
## Search View
##----------------------------------------------------------------##
class SearchView( EditorModule ):
	_name = 'search_view'
	_dependency = [ 'qt' ]

	def __init__( self ):
		self.enumerators = []
		self.onCancel    = None
		self.onSelection = None
		self.onSearch    = None
		self.onTest      = None
		self.visEntries  = None

	def onLoad( self ):
		self.window = SearchViewWidget( None )
		self.window.module = self

	def request( self, **option ):
		pass

##----------------------------------------------------------------##

searchView = SearchView()
searchView.register()

##----------------------------------------------------------------##