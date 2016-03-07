import sys
import os

from PySide import QtCore, QtGui
from PySide.QtCore import QEventLoop, QEvent, QObject, QSettings, QCoreApplication, QLocale

from time import time
import locale

from juma.core import *
import juma.themes

from QtEditorModule            	import QtEditorModule

##----------------------------------------------------------------##
class QtSupportEventFilter(QObject):
	def eventFilter(self, obj, event):
		e=event.type()
		if   e == QEvent.ApplicationActivate:
			signals.emitNow('app.activate')
		elif e == QEvent.ApplicationDeactivate:
			signals.emitNow('app.deactivate')		
		return QObject.eventFilter( self, obj, event )

##----------------------------------------------------------------##
class QtSupport( QtEditorModule ):
	def __init__( self ):
		self.statusWindow = None
		self.currentTheme = None

	def getName( self ):
		return 'qt'

	def getDependency( self ):
		return []

	def getBaseDependency( self ):
		return []

	def useStyle(self, style = ""):
		self.currentTheme = style
		self.applyTheme()

	def applyTheme(self):
		if self.currentTheme == "":
			self.qtApp.setStyleSheet("")
		else:
			self.qtApp.setStyleSheet( juma.themes.load_stylesheet(self.currentTheme) )

	def setupMainWindow( self ):
		self.mainWindow = QtMainWindow(None)
		self.mainWindow.setBaseSize( 800, 600 )
		self.mainWindow.resize( 800, 600 )
		self.mainWindow.setFixedSize(0,0)
		
		self.mainWindow.show()
		self.mainWindow.raise_() #bring app to front
		self.mainWindow.hide()
		self.mainWindow.module = self

		self.sharedMenuBar = QtGui.QMenuBar( None )
		self.mainWindow.setMenuWidget( self.sharedMenuBar )
		
		self.menu = self.addMenuBar( 'main', self.sharedMenuBar )
		self.menu.addChild('&File').addChild([
			'----',
			'E&xit',
			]
		)
		self.menu.addChild('&Edit')
		self.menu.addChild('&Window').addChild([
			'----',
			'Default Theme',
			'Dark Theme',
			'Robot Theme',
			'----',
			]
		)

	def getSharedMenubar( self ):
		return self.sharedMenuBar

	def showSystemStatusWindow( self ):
		pass
		# if not self.statusWindow:
		# 	self.statusWindow = self.requestSubWindow( 'SystemStatus',
		# 			title     = 'System Status',
		# 			size      = (200,200),
		# 			minSize   = (200,200)
		# 		)
		# 	self.statusWindow.body = self.statusWindow.addWidgetFromFile(
		# 			self.getApp().getPath( 'data/ui/SystemStatus.ui' )
		# 		)
		# self.statusWindow.show()
		# self.statusWindow.raise_()

	def setActiveWindow(self, window):
		self.qtApp.setActiveWindow(window)

	def onLoad( self ):
		QLocale.setDefault(QLocale(QLocale.C))
		locale.setlocale(locale.LC_ALL, 'C')

		QCoreApplication.setOrganizationName("CloudTeam")
		QCoreApplication.setOrganizationDomain("cloudteam.pro")
		QCoreApplication.setApplicationName("JUMA Editor")

		self.qtApp = QtGui.QApplication( sys.argv )
		self.qtSetting = QtCore.QSettings()
		
		self.setupMainWindow()		

		self.initialized = True
		self.running     = False
		return True

	def onStart( self ):
		eventFilter = QtSupportEventFilter( self.qtApp )
		eventFilter.app = self
		self.qtApp.installEventFilter(eventFilter)

	def needUpdate( self ):
		return True

	def onUpdate( self ):
		if not self.qtApp.hasPendingEvents(): return
		self.qtApp.processEvents( QEventLoop.AllEvents, 4 )
	
	def getMainWindow( self ):
		return self.mainWindow

	def getQtSettingObject( self ):
		return self.qtSetting
	
	def onStart( self ):	
		self.restoreWindowState( self.mainWindow )
		self.currentTheme = self.qtSetting.value("theme/style", 'darkstyle')
		self.applyTheme()
		self.qtApp.processEvents( QEventLoop.AllEvents )

	def onStop( self ):
		self.qtSetting.setValue("theme/style", self.currentTheme)
		self.saveWindowState( self.mainWindow )

	def onMenu(self, node):
		name = node.name
		if name == 'exit':
			self.getApp().stop()
		elif name == 'default_theme':
			self.useStyle()
		elif name == 'dark_theme':
			self.useStyle( 'darkstyle' )
		elif name == 'robot_theme':
			self.useStyle( 'robotstyle' )
		# elif name == 'system_status':
		# 	self.showSystemStatusWindow()
		# elif name == 'asset_editor':
		# 	self.getModule('asset_editor').setFocus()
		# elif name == 'scene_editor':
		# 	self.getModule('scene_editor').setFocus()
		# elif name == 'debug_view':
		# 	self.getModule('debug_view').setFocus()
		# elif name == 'refresh_theme':
		# 	self.setupStyle()
		# elif name == 'copy':
		# 	print 'copy'
		# elif name == 'paste':
		# 	print 'paste'
		# elif name == 'cut':
		# 	print 'cut'

		# elif name == 'undo':
		# 	stack = EditorCommandRegistry.get().getCommandStack( 'scene_editor' )
		# 	stack.undoCommand()

		# elif name == 'redo':
		# 	stack = EditorCommandRegistry.get().getCommandStack( 'scene_editor' )
		# 	stack.redoCommand()

	

QtSupport().register()

##----------------------------------------------------------------##
class QtMainWindow( QtGui.QMainWindow ):
	"""docstring for QtMainWindow"""
	def __init__(self, parent,*args):
		super(QtMainWindow, self).__init__(parent, *args)
	
	def closeEvent(self,event):
		if self.module.alive:
			self.hide()
			event.ignore()
		else:
			pass

##----------------------------------------------------------------##
class QtGlobalModule( QtEditorModule ):
	"""docstring for QtGlobalModule"""
	def getMainWindow( self ):
		qt = self.getQtSupport()
		return qt.getMainWindow()

	def requestDockWindow( self, id = None, **windowOption ):
		raise Exception( 'only subwindow supported for globalModule' )

	def requestDocumentWindow( self, id = None, **windowOption ):
		raise Exception( 'only subwindow supported for globalModule' )

	def requestSubWindow( self, id = None, **windowOption ):
		if not id: id = self.getName()
		mainWindow = self.getMainWindow()
		container = mainWindow.requestSubWindow( id, **windowOption )
		# self.containers[id] = container
		return container
		