#!/usr/bin/env python

from PySide import QtCore, QtGui
from PySide.QtCore import QSettings

from juma.core import signals
from juma.moai import *

##----------------------------------------------------------------##
class LayerWidget( QtGui.QWidget ):
    workingDir = None
    runningFile = None

    def __init__( self, parent=None ):
        super(LayerWidget, self).__init__( parent )
        self.setObjectName("LayerWidget")
        self.lid = 'layer_none'

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.initUI()

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)

        self.moaiWidget = MOAIWidget()
        self.scrollArea.setWidget(self.moaiWidget)

        layout.addWidget( self.toolBar )
        layout.addWidget( self.scrollArea )

    def initUI(self):
        self.toolBar = self.createToolBar()

        openAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton), '&Open', self)
        openAction.triggered.connect(self.openFolder)
        self.toolBar.addAction(openAction)

        reloadAction = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_BrowserReload), '&Reload', self)
        reloadAction.triggered.connect(self.reload)
        self.toolBar.addAction(reloadAction)

        floatValidator = QtGui.QDoubleValidator()
        floatValidator.setRange(128, 4096)

        widthLabel = QtGui.QLabel()
        widthLabel.setText("W:")
        self.toolBar.addWidget(widthLabel)

        self.widthEdit = QtGui.QLineEdit()
        self.widthEdit.setFixedWidth(50)
        self.widthEdit.setText('320')
        self.widthEdit.setValidator(floatValidator)
        self.widthEdit.textChanged.connect(self.viewSizeEditingFinished)
        self.toolBar.addWidget(self.widthEdit)

        heightLabel = QtGui.QLabel()
        heightLabel.setText("H:")
        self.toolBar.addWidget(heightLabel)

        self.heightEdit = QtGui.QLineEdit()
        self.heightEdit.setFixedWidth(50)
        self.heightEdit.setText('480')
        self.heightEdit.setValidator(floatValidator)
        self.heightEdit.textChanged.connect(self.viewSizeEditingFinished)
        self.toolBar.addWidget(self.heightEdit)

        comboSize = QtGui.QComboBox()
        comboSize.addItems(["Custom", "320x480", "480x320", "640x960", "960x640", "368x512", "512x368"])
        self.toolBar.addWidget(comboSize)

    def createToolBar(self):
        toolbar = QtGui.QToolBar()
        return toolbar

    def setLayerId(self, lid):
        self.lid = lid

    def readSettings(self):
        settings = QSettings()

        glSize = self.moaiWidget.sizeHint()
        
        self.widthEdit.setText( settings.value("editor/%s/width" % self.lid, str(glSize.width())) )
        self.heightEdit.setText( settings.value("editor/%s/height" % self.lid, str(glSize.height())) )
        self.runningFile = settings.value("editor/%s/currentFile" % self.lid)
        self.workingDir = settings.value("editor/%s/workingDir" % self.lid, "")

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("editor/%s/height" % self.lid, self.widthEdit.text())
        settings.setValue("editor/%s/height" % self.lid, self.heightEdit.text())
        settings.setValue("editor/%s/runningFile" % self.lid, self.runningFile)
        settings.setValue("editor/%s/workingDir" % self.lid, self.workingDir)

    def start(self):
        if self.runningFile:
            self.moaiWidget.runScript( self.runningFile )

    def pause(self, value):
        pass

    def stop(self):
        pass

    def moai(self):
        return self.moaiWidget

    def openFolder(self):
        signals.emitNow('app.open_file')

    def reload(self):
        if self.workingDir and self.runningFile:
            self.openFile(self.runningFile, self.workingDir)

    def resize(self, width, height):
        self.moaiWidget.resize(width, height)

    def openFile(self, fileName, workingDir = ""):
        # self.statsDock.stopTimer()
        print("Open File...")

        self.moaiWidget.refreshContext()
        self.moaiWidget.setWorkingDirectory(workingDir)
        self.moaiWidget.setTraceback(tracebackFunc)
        self.moaiWidget.setPrint(luaBeforePrint, luaAfterPrint)
        
        self.moaiWidget.loadEditorFramework()

        # self.debugDock.updateAllDebugValues()
        # self.environmentDock.applyEnvironmentSettings()
        # self.profilerDock.applyProfilingSettings()
        
        self.moaiWidget.loadLuaFramework()
        
        self.runningFile = fileName
        self.workingDir = workingDir
        self.start()

        # self.environmentDock.startSession(False)

        # self.livereload.lua = self.moaiWidget.lua
        # self.consoleDialog.lua = self.moaiWidget.lua
        # self.livereload.watchDirectory(workingDir)

        # self.statsDock.setLuaState(self.moaiWidget.lua)
        # self.statsDock.startTimer()

        # self.runAttempts = 0
        # settings = QSettings()
        # settings.setValue("main/openProjectAttempts", self.runAttempts)
    
    def viewSizeEditingFinished(self):
        try:
            width = float(self.widthEdit.text())
        except ValueError:
            width = 640

        try:
            height = float(self.heightEdit.text())
        except ValueError:
            height = 480

        self.resize(width, height)