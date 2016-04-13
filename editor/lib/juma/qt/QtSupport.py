import sys
import os

from PySide import QtCore, QtGui
from PySide.QtCore import QEventLoop, QEvent, QObject, QSettings, QCoreApplication, QLocale
from PySide.QtGui import QFileDialog

from time import time
import locale

from juma.core import *
import themes

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
	_name = "qt"
	_dependency = []

	statusWindow = None
	currentTheme = None

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
			'Open Project',
			'----',
			'E&xit',
			]
		)
		self.menu.addChild('&Edit').addChild( [
			'Undo|Ctrl+Z',
			'Redo|Ctrl+Shift+Z',
			'----',
			]
		)
		self.menu.addChild('&Asset')
		self.menu.addChild( dict( name = 'preview', label = 'Game' ) )
		self.menu.addChild('&Entity')
		self.menu.addChild('&View').addChild([
			'----',
			'Default Theme',
			'Dark Theme',
			'Robot Theme',
			'----',
			]
		)
		self.menu.addChild('&Window').addChild([
			'----',
			'Main Editor|F2',
			'----',
			'Game Preview',
			'Hierarchy',
			'Introspector',
			'Stats Viewer',
			'Debug Draw',
			'Run String Dock',
			'----',
			]
		)
		# self.menu.addChild('&Help')

	def getSharedMenubar( self ):
		return self.sharedMenuBar

	def showSystemStatusWindow( self ):
		pass # this method use gii

	def setActiveWindow(self, window):
		self.qtApp.setActiveWindow(window)

	def getMainWindow( self ):
		return self.mainWindow

	def getQtSettingObject( self ):
		return self.qtSetting

	##----------------------------------------------------------------##
	def openProject( self ):
		fileName, filt = QFileDialog.getOpenFileName(self.mainWindow, "Open Project File", "~", "Project file (*.json )")
		if fileName:
			path = os.path.dirname( fileName )
			self.getApp().openProject( path )

	def useStyle( self, style = "" ):
		self.currentTheme = style
		self.applyTheme()

	def applyTheme( self ):
		if self.currentTheme == "":
			self.qtApp.setStyleSheet("")
		else:
			self.qtApp.setStyleSheet( themes.load_stylesheet(self.currentTheme) )
	
	##----------------------------------------------------------------##
	def onLoad( self ):
		QLocale.setDefault(QLocale(QLocale.C))
		locale.setlocale(locale.LC_ALL, 'C')

		QCoreApplication.setOrganizationName("CloudTeam")
		QCoreApplication.setOrganizationDomain("cloudteam.pro")
		QCoreApplication.setApplicationName("juma-moai-editor")

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

	def onStart( self ):	
		self.restoreWindowState( self.mainWindow )
		self.getApp().openProject( self.qtSetting.value("project/path", '~') )
		self.currentTheme = self.qtSetting.value("theme/style", 'robotstyle')
		self.applyTheme()
		self.qtApp.processEvents( QEventLoop.AllEvents )

	def onStop( self ):
		self.qtSetting.setValue("theme/style", self.currentTheme)
		self.qtSetting.setValue("project/path", self.getProject().path )
		self.saveWindowState( self.mainWindow )

	def onMenu(self, node):
		name = node.name
		if name == 'exit':
			self.getApp().stop()

		if name == 'open_project':
			self.openProject()

		elif name == 'default_theme':
			self.useStyle()
		elif name == 'dark_theme':
			self.useStyle( 'darkstyle' )
		elif name == 'robot_theme':
			self.useStyle( 'robotstyle' )

		elif name == 'main_editor':
			self.getModule('main_editor').setFocus()

		elif name == 'game_preview':
			self.getModule('game_preview').show()

		elif name == 'hierarchy':
			self.getModule('graph_editor').show()
		elif name == 'introspector':
			self.getModule('introspector').show()

		elif name == 'stats_viewer':
			self.getModule('stats_viewer').show()
		elif name == 'run_string_dock':
			self.getModule('run_string_dock').show()
		elif name == 'debug_draw':
			self.getModule('debug_draw_dock').show()

		elif name == 'copy':
			print 'copy'
		elif name == 'paste':
			print 'paste'
		elif name == 'cut':
			print 'cut'

		elif name == 'undo':
			stack = EditorCommandRegistry.get().getCommandStack( 'main_editor' )
			stack.undoCommand()

		elif name == 'redo':
			stack = EditorCommandRegistry.get().getCommandStack( 'main_editor' )
			stack.redoCommand()

##----------------------------------------------------------------##

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
		