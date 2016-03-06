#!/usr/bin/env python

import os

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings, QCoreApplication, QLocale

from juma.qt.helpers.helper import restrainWidgetToScreen

from juma.core import signals
from juma.qt.controls.Menu import MenuManager
from juma.qt.controls.Layers import LayerWidget

import juma.themes

def getWindowScreenId(window):
    desktop=QtGui.QApplication.desktop()
    return desktop.screenNumber(window)
    
def moveWindowToCenter(window):
    desktop=QtGui.QApplication.desktop()
    geom=desktop.availableGeometry(window)
    x=(geom.width()-window.width())/2 +geom.x()
    y=(geom.height()-window.height())/2+geom.y()
    window.move(x,y)

##----------------------------------------------------------------##
class MainWindow( QMainWindow ):
    def __init__(self, parent=None, script=None):
        super(MainWindow, self).__init__(parent)

        QtCore.QCoreApplication.instance().mainWindow = self

        self.setObjectName("MainWindow")
        self.setUnifiedTitleAndToolBarOnMac( False )
        self.setDockOptions( QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AllowTabbedDocks )
        self.setDockNestingEnabled(True)
        self.setWindowModality(QtCore.Qt.NonModal)
        # self.resize(800, 600)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.defaultToolBarIconSize = 12
        self.setIconSize( QtCore.QSize( 12, 12 ) )

        font=QtGui.QFont()
        font.setPointSize(11)
        self.setFont(font)

        signals.connect( 'app.open_file', self.onAppOpenFile )

        layout = QtGui.QVBoxLayout( None )
        self.setLayout(layout)

        self.layersEditor = LayersEditor( None )
        self.sharedToolBar = QtGui.QToolBar( None )

        layout.addWidget( self.sharedToolBar )
        layout.addWidget( self.layersEditor )
        self.setCentralWidget( layout )

        # self.centerEditor.newLayer()

        self.readSettings()

    def moveToCenter(self):
        moveWindowToCenter(self)

    def ensureVisible(self):
        restrainWidgetToScreen(self)

    def readSettings(self):
        settings = QSettings()

        self.currentTheme = settings.value("main/theme", 'darkstyle')
        self.applyTheme()
        self.restoreGeometry(settings.value("main/geometry"))
        self.restoreState(settings.value("main/windowState"))

        self.layersEditor.readSettings()

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("main/theme", self.currentTheme)
        settings.setValue("main/geometry", self.saveGeometry())
        settings.setValue("main/windowState", self.saveState())

        self.layersEditor.writeSettings()

    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

    def useDefaultStyle(self):
        self.currentTheme = ""
        self.applyTheme()

    def useDarkStyle(self):
        self.currentTheme = 'darkstyle'
        self.applyTheme()

    def applyTheme(self):
        if self.currentTheme == "":
            self.setStyleSheet("")
        else:
            self.setStyleSheet(themes.load_stylesheet(self.currentTheme))

    def onAppOpenFile(self):
        layer = self.layersEditor.currentLayer()
        if layer:
            fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", layer.workingDir or "~", "Lua source (*.lua )")
            if fileName:
                workingDir = os.path.dirname(fileName)
                luaFile = os.path.basename(fileName)
                layer.openFile(luaFile, workingDir)


##----------------------------------------------------------------##
class LayersEditor( QtGui.QTabWidget ):
    layers = 0

    def __init__(self, parent=None):
        super(LayersEditor, self).__init__( parent )

        self.setObjectName("LayersEditor")

        self.setTabsClosable(True)
        self.setMovable(False)
        self.currentChanged.connect(self.onTabBarChange)
        self.tabCloseRequested.connect(self.onTabBarClose)

    def newLayer(self):
        layer = LayerWidget()
        self.addLayer( layer )
        layer.start()
    
    def addLayer(self, widget, name=""):
        self.layers += 1
        layerName = '%s Layer' % name
        widget.setLayerId('layer_%d' % self.layers)
        if name == "":
            layerName = 'Layer %d' % self.layers
        self.addTab( widget, layerName )

    def currentLayer(self):
        return self.currentWidget()

    def readSettings(self):
        settings = QSettings()

        self.restoreGeometry(settings.value("layerseditor/geometry"))
        # self.restoreState(settings.value("layerseditor/windowState"))

        # FIXME for all layers opened
        self.currentLayer().readSettings()

    def writeSettings(self):
        settings = QSettings()

        settings.setValue("layerseditor/geometry", self.saveGeometry())
        # settings.setValue("layerseditor/windowState", self.saveState())

        # FIXME for all layers opened
        self.currentLayer().writeSettings()

    def onTabBarChange(self, index):
        print("tabBar changed", index)

    def onTabBarClose(self, index):
        print("tabBar closed", index)



##----------------------------------------------------------------##
class SubWindowMixin:
    def createContainer(self):
        container = QtGui.QWidget(self)
        self.setWidget(container)
        return container

    def moveToCenter(self):
        moveWindowToCenter(self)

    def ensureVisible(self):
        restrainWidgetToScreen(self)