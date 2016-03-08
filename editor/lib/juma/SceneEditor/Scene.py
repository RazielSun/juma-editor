#!/usr/bin/env python
from abc        import ABCMeta, abstractmethod

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.moai import *

##----------------------------------------------------------------##
class SceneObject(object):
	_width = 640
	_height = 480
	_dir_path = ""
	_source = None

	def __init__(self):
		pass

	def setSize(self, width, height):
		self._width = width
		self._height = height

	def setSource(self, source, dir_path):
		self._source = source
		self._dir_path = dir_path

	def width(self):
		return self._width

	def height(self):
		return self._height

	def source(self):
		return self._source

	def dir(self):
		return self._dir_path

##----------------------------------------------------------------##
class Scene( QtGui.QScrollArea ):
	_name = 'Scene'
	_type = None
	_object = None
	_started = False

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

	def getName( self ):
		return self._name

	def setObject( self, obj ):
		if obj:
			self._object = obj

	def obj(self):
		return self._object

	def getType(self):
		return self._type

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

	def start( self ):
		if not self._started:
			self.reload()
			self._started = True

	def pause( self ):
		pass

	def stop( self ):
		pass

	def reload( self ):
		obj_ = self.obj()
		if obj_ and obj_.source():
			self.openFile( obj_.source(), obj_.dir() )

	def resize( self, width, height ):
		obj_ = self.obj()
		if obj_:
			obj_.setSize( width, height )
			self.moaiWidget.resize( obj_.width(), obj_.height() )

	def openProject( self ):
		obj_ = self.obj()
		fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", obj_.dir() or "~", "Lua source (*.lua )")
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

		obj_ = self.obj()
		obj_.setSource( filename, workingDir )
		self.moaiWidget.runScript( obj_.source() )

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

def getSceneByType( type ):
	scene = None
	if type == 'moai':
		scene = SceneMOAI( None )

	return scene