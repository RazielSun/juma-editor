#!/usr/bin/env python
from abc        import ABCMeta, abstractmethod

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.moai import *

##----------------------------------------------------------------##
class SceneObject(object):
	_type = None
	_width = 100
	_height = 100
	_workingDir = None
	_runningFile = None

	def __init__(self):
		pass

##----------------------------------------------------------------##
class Scene( QtGui.QScrollArea ):
	_object = None
	_type = None
	_name = 'Scene'
	_width = 100
	_height = 100
	_workingDir = None
	_runningFile = None

	def __init__( self, parent=None ):
		super(Scene, self).__init__( parent )

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.moaiWidget = MOAIWidget()
		self.setWidget(self.moaiWidget)

	def moai(self):
		return self.moaiWidget

	@abstractmethod
	def setName( self, index ):
		self._name = 'Scene {}'.format(index)

	@abstractmethod
	def getName( self ):
		return self._name

	@abstractmethod
	def start( self ):
		pass

	@abstractmethod
	def pause( self ):
		pass

	@abstractmethod
	def stop( self ):
		pass

	@abstractmethod
	def reload( self ):
		pass

	@abstractmethod
	def resize( self, width, height ):
		pass

	@abstractmethod
	def openProject( self ):
		pass

	@abstractmethod
	def openFile( self, filename, workingDir = "" ):
		pass

##----------------------------------------------------------------##
class SceneMOAI( Scene ):
	_type = 'moai'

	def __init__( self, parent=None ):
		super(SceneMOAI, self).__init__( parent )

	def setName( self, index ):
		self._name = 'MOAI {}'.format(index)

	def getName( self ):
		return self._name

	def start( self ):
		if self._runningFile:
			self.moaiWidget.runScript( self._runningFile )

	def pause( self ):
		pass

	def stop( self ):
		pass

	def reload( self ):
		if self._workingDir and self._runningFile:
			self.openFile( self._runningFile, self._workingDir )

	def resize( self, width, height ):
		self.moaiWidget.resize( width, height )

	def openProject( self ):
		fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", self._workingDir or "~", "Lua source (*.lua )")
		if fileName:
			dir_path = os.path.dirname(fileName)
			file_path = os.path.basename(fileName)
			self.openFile( file_path, dir_path )

	def openFile( self, filename, workingDir = "" ):
		self.moaiWidget.refreshContext()
		self.moaiWidget.setWorkingDirectory( workingDir )
		self.moaiWidget.setTraceback( tracebackFunc )
		self.moaiWidget.setPrint( luaBeforePrint, luaAfterPrint )

		self.moaiWidget.loadEditorFramework()
		self.moaiWidget.loadLuaFramework()

		self._runningFile = filename
		self._workingDir = workingDir
		self.start()

    # def readSettings(self):
    #     settings = QSettings()

    #     glSize = self.moaiWidget.sizeHint()
        
#         self.widthEdit.setText( settings.value("editor/%s/width" % self.lid, str(glSize.width())) )
#         self.heightEdit.setText( settings.value("editor/%s/height" % self.lid, str(glSize.height())) )
#         self.runningFile = settings.value("editor/%s/currentFile" % self.lid)
#         self.workingDir = settings.value("editor/%s/workingDir" % self.lid, "")

#     def writeSettings(self):
#         settings = QSettings()

#         settings.setValue("editor/%s/height" % self.lid, self.widthEdit.text())
#         settings.setValue("editor/%s/height" % self.lid, self.heightEdit.text())
#         settings.setValue("editor/%s/runningFile" % self.lid, self.runningFile)
#         settings.setValue("editor/%s/workingDir" % self.lid, self.workingDir)

#     def openFile(self, fileName, workingDir = ""):
#         # self.statsDock.stopTimer()
#         print("Open File...")

#         self.moaiWidget.refreshContext()
#         self.moaiWidget.setWorkingDirectory(workingDir)
#         self.moaiWidget.setTraceback(tracebackFunc)
#         self.moaiWidget.setPrint(luaBeforePrint, luaAfterPrint)
        
#         self.moaiWidget.loadEditorFramework()

#         # self.debugDock.updateAllDebugValues()
#         # self.environmentDock.applyEnvironmentSettings()
#         # self.profilerDock.applyProfilingSettings()
        
#         self.moaiWidget.loadLuaFramework()
        
#         self.runningFile = fileName
#         self.workingDir = workingDir
#         self.start()

#         # self.environmentDock.startSession(False)

#         # self.livereload.lua = self.moaiWidget.lua
#         # self.consoleDialog.lua = self.moaiWidget.lua
#         # self.livereload.watchDirectory(workingDir)

#         # self.statsDock.setLuaState(self.moaiWidget.lua)
#         # self.statsDock.startTimer()

#         # self.runAttempts = 0
#         # settings = QSettings()
#         # settings.setValue("main/openProjectAttempts", self.runAttempts)
    