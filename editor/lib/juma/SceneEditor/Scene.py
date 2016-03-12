#!/usr/bin/env python
from abc        import ABCMeta, abstractmethod
import os

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.moai import *

##----------------------------------------------------------------##
class SceneHeader(object):
	_width = 640
	_height = 480
	_dir_path = ""
	_source = None

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

	def full_path(self):
		return os.path.join( self._dir_path, self._source )

##----------------------------------------------------------------##
class SceneProject(object):
	_type = 'moai'
	_header = None

	def getType(self):
		return self._type

	# Header
	def setHeader( self, header ):
		if header:
			self._header = header

	def head(self):
		return self._header
##----------------------------------------------------------------##
class Scene( QtGui.QScrollArea ):
	_sid = -1
	_name = 'None'
	_project = None
	_started = False

	colorPrintEnabled = True

	def __init__( self, parent=None ):
		super(Scene, self).__init__( parent )

		self._project = SceneProject()

		self.setBackgroundRole(QtGui.QPalette.Dark)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self.moaiWidget = MOAIWidget()
		self.setWidget(self.moaiWidget)

	def moai(self):
		return self.moaiWidget

	# Names and types
	def setSId( self, index ):
		self._sid = index
		self.setName('Moai {}'.format(index))

	def setName( self, name ):
		self._name = name

	def getName( self ):
		return self._name

	# Scene Header and Project
	def setHeader( self, header ):
		self._project.setHeader( header )
		obj_ = self.head()
		if obj_:
			self.moaiWidget.resize( obj_.width(), obj_.height() )

	def head(self):
		return self._project.head()

	def setProject( self, project ):
		self._project = project

	def project( self ):
		return self._project
	
	# Lifecycle methods
	@abstractmethod
	def start( self ):
		self.moaiWidget.setupContext()
		if not self._started:
			self.reload()
			self._started = True
		self.moaiWidget.makeCurrent()
		signals.emitNow( 'scene.start', self._sid )

	@abstractmethod
	def pause( self ):
		# self.moaiWidget.pause( True )
		signals.emitNow( 'scene.pause', self._sid )

	@abstractmethod
	def stop( self ):
		signals.emitNow( 'scene.stop', self._sid )
		# self.moaiWidget.deleteContext()

	# Methods
	@abstractmethod
	def reload( self ):
		obj_ = self.head()
		if obj_ and obj_.source():
			printSeparator( obj_.full_path(), self.colorPrintEnabled )
			self.openFile( obj_.source(), obj_.dir() )

	@abstractmethod
	def resize( self, width, height ):
		success = False
		obj_ = self.head()
		if obj_:
			if width != obj_.width() or height != obj_.height():
				obj_.setSize( width, height )
				self.moaiWidget.resize( obj_.width(), obj_.height() )
				success = True
		return success

	@abstractmethod
	def openSource( self ):
		obj_ = self.head()
		fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", obj_.dir() or "~", "Lua source (*.lua )")
		if fileName:
			dir_path = os.path.dirname(fileName)
			file_path = os.path.basename(fileName)
			self.openFile( file_path, dir_path )

	@abstractmethod
	def openFile( self, filename, workingDir = "" ):
		signals.emitNow( 'scene.pre_open_source', self._sid )
		
		self.moaiWidget.refreshContext()
		self.moaiWidget.setWorkingDirectory( workingDir )
		self.moaiWidget.setTraceback( tracebackFunc )
		self.moaiWidget.setPrint( luaBeforePrint, luaAfterPrint )

		obj_ = self.head()
		obj_.setSource( filename, workingDir )

		self.moaiWidget.loadEditorFramework()
		self.moaiWidget.loadLuaFramework( workingDir )
		self.moaiWidget.runScript( obj_.source() )

		self.moaiWidget.initReady = True

		signals.emitNow( 'scene.open_source', self._sid )

##----------------------------------------------------------------##

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
		scene = Scene( None )

	return scene