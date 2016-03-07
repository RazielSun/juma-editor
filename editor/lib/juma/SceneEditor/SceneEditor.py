#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui
from PySide.QtCore import QEventLoop, QEvent, QObject, QSettings, QCoreApplication, QLocale

from time import time
import locale

from juma.core import *
import juma.themes
from juma.qt.controls.Window    import MainWindow
from juma.qt.QtEditorModule     import QtEditorModule

from SceneWidgets               import SceneSizeComboBox

##----------------------------------------------------------------##
class SceneEditor( QtEditorModule ):
    _name       = 'scene_editor'
    _dependency = ['qt']

    def __init__( self ):
        pass

    def setupMainWindow( self ):
        self.mainWindow = QtMainWindow(None)
        self.mainWindow.setBaseSize( 800, 600 )
        self.mainWindow.resize( 800, 600 )
        self.mainWindow.setWindowTitle( 'Scene Editor' )
        self.mainWindow.setMenuWidget( self.getQtSupport().getSharedMenubar() )
        self.mainWindow.module = self

        self.newScene()
        
        self.mainToolBar = self.addToolBar( 'scene', self.mainWindow.requestToolBar( 'main' ) )     
        self.statusBar = QtGui.QStatusBar()
        self.mainWindow.setStatusBar(self.statusBar)

    def onLoad( self ):
        self.setupMainWindow()
        self.containers  = {}

        self.sceneSizeWidget = SceneSizeComboBox( None )
        self.sceneSizeWidget.owner = self

        self.findMenu( 'main/file' ).addChild([
            dict( name = 'open_scene', label = 'Open', shortcut = 'ctrl+O' ),
        ], self )

        self.findMenu( 'main/edit' ).addChild([
            dict( name = 'reload_scene', label = 'Reload', shortcut = 'ctrl+R' ),
        ], self )

        self.addTool( 'scene/open_scene', label = 'Open', menuLink = 'main/file/open_scene', icon = 'folder' )
        self.addTool( 'scene/reload_scene', label = 'Reload', menuLink = 'main/edit/reload_scene', icon = 'repeat' )
        self.addTool( 'scene/size_scene', widget = self.sceneSizeWidget )

        return True

    def onStart( self ):
        self.setFocus()
        self.restoreWindowState( self.mainWindow )
    
    def onStop( self ):
        self.saveWindowState( self.mainWindow )

    #controls
    def onSetFocus(self):
        self.mainWindow.show()
        self.mainWindow.raise_()
        self.mainWindow.setFocus()

    #resource provider
    # def requestDockWindow( self, id, **dockOptions ):
    #     container = self.mainWindow.requestDockWindow(id, **dockOptions)        
    #     self.containers[id] = container
    #     return container

    # def requestSubWindow( self, id, **windowOption ):
    #     container = self.mainWindow.requestSubWindow(id, **windowOption)        
    #     self.containers[id] = container
    #     return container

    # def requestDocumentWindow( self, id, **windowOption ):
    #     container = self.mainWindow.requestDocuemntWindow(id, **windowOption)
    #     self.containers[id] = container
    #     return container

    def getMainWindow( self ):
        return self.mainWindow

    def onMenu(self, node):
        name = node.name

    def onTool(self, node):
        name = node.name
        # print("SceneEditor: onTool:", name)

    # Scene methods
    def getTab(self):
        return self.mainWindow.centralWidget()

    def newScene(self):
        scene = QtGui.QWidget( None )
        name = 'Scene 1'
        self.addScene( scene, name )

    def addScene(self, scene, name):
        tab = self.getTab()
        tab.addTab( scene, name )

class QtMainWindow( MainWindow ):
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
class SceneEditorModule( QtEditorModule ):
    def getMainWindow( self ):
        return self.getModule('scene_editor').getMainWindow()

##----------------------------------------------------------------##
SceneEditor().register()


##----------------------------------------------------------------##
# class TabSceneEditor( QtGui.QTabWidget ):
#     scenes = 0

#     def __init__(self, parent=None):
#         super(TabSceneEditor, self).__init__( parent )

#         self.setObjectName("TabSceneEditor")

#         self.setTabsClosable(True)
#         self.setMovable(False)
#         self.currentChanged.connect(self.onTabBarChange)
#         self.tabCloseRequested.connect(self.onTabBarClose)

    # def newLayer(self):
    #     layer = LayerWidget()
    #     self.addLayer( layer )
    #     layer.start()
    
    # def addLayer(self, widget, name=""):
    #     self.layers += 1
    #     layerName = '%s Layer' % name
    #     widget.setLayerId('layer_%d' % self.layers)
    #     if name == "":
    #         layerName = 'Layer %d' % self.layers
    #     self.addTab( widget, layerName )

    # def currentLayer(self):
    #     return self.currentWidget()

    # def readSettings(self):
    #     settings = QSettings()

    #     self.restoreGeometry(settings.value("layerseditor/geometry"))
    #     # self.restoreState(settings.value("layerseditor/windowState"))

    #     # FIXME for all layers opened
    #     self.currentLayer().readSettings()

    # def writeSettings(self):
    #     settings = QSettings()

    #     settings.setValue("layerseditor/geometry", self.saveGeometry())
    #     # settings.setValue("layerseditor/windowState", self.saveState())

    #     # FIXME for all layers opened
    #     self.currentLayer().writeSettings()

    # def onTabBarChange(self, index):
    #     print("tabBar changed", index)

    # def onTabBarClose(self, index):
    #     print("tabBar closed", index)
        