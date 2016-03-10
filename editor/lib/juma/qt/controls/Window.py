#!/usr/bin/env python

import os

from PySide import QtCore, QtGui
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtCore import QSettings, QCoreApplication, QLocale

from juma.qt.helpers.helper import restrainWidgetToScreen

from juma.core import signals
from juma.qt.controls.Menu import MenuManager
from juma.qt.controls.Layers import LayerWidget

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

        self.setWindowTitle( 'JUMA' )

        self.setBaseSize( 800, 600 )
        self.resize( 800, 600 )

        self.setUnifiedTitleAndToolBarOnMac( False )
        self.setDockOptions( QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AllowTabbedDocks )
        self.setDockNestingEnabled(True)
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setMouseTracking(True)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.defaultToolBarIconSize = 16
        font=QtGui.QFont()
        font.setPointSize(11)
        self.setFont(font)

        self.tabWidget = QtGui.QTabWidget( None )
        self.tabWidget.setTabsClosable( True )
        self.tabWidget.setMovable( False )
        # self.tabWidget.setDocumentMode( True )

        self.setCentralWidget( self.tabWidget )

    def moveToCenter(self):
        moveWindowToCenter( self )

    def ensureVisible(self):
        restrainWidgetToScreen( self )

    def requestToolBar( self, name, **options ):
        toolbar = QtGui.QToolBar()
        toolbar.setFloatable( options.get( 'floatable', False ) )
        toolbar.setMovable(   options.get( 'movable',   False ) )        
        toolbar.setObjectName( 'toolbar-%s' % name )
        iconSize = options.get('icon_size', self.defaultToolBarIconSize )
        self.addToolBar( toolbar )
        toolbar.setIconSize( QtCore.QSize( iconSize, iconSize ) )
        toolbar._icon_size = iconSize
        return toolbar

    # def onAppOpenFile(self):
    #     layer = self.layersEditor.currentLayer()
    #     if layer:
    #         fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "Run Script", layer.workingDir or "~", "Lua source (*.lua )")
    #         if fileName:
    #             workingDir = os.path.dirname(fileName)
    #             luaFile = os.path.basename(fileName)
    #             layer.openFile(luaFile, workingDir)

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