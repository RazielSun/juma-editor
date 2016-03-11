#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.qt.TopEditorModule    import TopEditorModule, QtMainWindow, SubEditorModule

from Scene                      import SceneObject, getSceneByType
from SceneWidgets               import SceneSizeComboBox

##----------------------------------------------------------------##
class SceneEditor( TopEditorModule ):
    _name       = 'scene_editor'
    _dependency = ['qt']
    _scenes = 0
    _currentIndex = -1

    def getWindowTitle( self ):
        return 'Scene Editor'

    def onLoad( self ):
        self.mainWindow.setMenuWidget( self.getQtSupport().getSharedMenubar() )
        
        self.mainToolBar = self.addToolBar( 'scene', self.mainWindow.requestToolBar( 'main' ) )     

        self.getTab().currentChanged.connect(self.onSceneChanged)
        self.getTab().tabCloseRequested.connect(self.onSceneCloseRequested)
        self.containers  = {}

        self.sceneSizeWidget = SceneSizeComboBox( None )
        self.sceneSizeWidget.owner = self

        self.findMenu( 'main/file' ).addChild([
            dict( name = 'new_scene_moai', label = 'New MOAI...', shortcut = 'ctrl+N' ),
            dict( name = 'open_scene', label = 'Open', shortcut = 'ctrl+O' ),
        ], self )

        self.findMenu( 'main/edit' ).addChild([
            dict( name = 'reload_scene', label = 'Reload', shortcut = 'ctrl+R' ),
        ], self )

        self.addTool( 'scene/new_scene_moai', label = 'New MOAI', menu_link = 'main/file/new_scene_moai', icon = 'file' )
        self.addTool( 'scene/open_scene', label = 'Open', menu_link = 'main/file/open_scene', icon = 'folder' )
        self.addTool( 'scene/reload_scene', label = 'Reload', menu_link = 'main/edit/reload_scene', icon = 'repeat' )
        self.addTool( 'scene/size_scene', widget = self.sceneSizeWidget )

        signals.connect( 'scene.change_size', self.sceneChangeSize )

        return True

    def onStart( self ):
        self.setFocus()
        self.restoreWindowState( self.mainWindow )

    # Save and Restore States
    def saveWindowState( self, window ):
        super(SceneEditor, self).saveWindowState( window )
        settings = self.getQtSettingObject()
        tab = self.getTab()
        settings.beginWriteArray(self.getName() + '_tab_widgets')
        for i in range(tab.count()):
            settings.setArrayIndex(i)
            scene = tab.widget(i)
            settings.setValue( "type", scene.getType() )
            obj_ = scene.obj()
            settings.setValue( "object", obj_ )
        settings.endArray()

    def restoreWindowState( self, window ):
        super(SceneEditor, self).restoreWindowState( window )
        settings = self.getQtSettingObject()
        size = settings.beginReadArray(self.getName() + '_tab_widgets')
        for i in range(size):
            settings.setArrayIndex(i)
            type = settings.value( "type" )
            scene = getSceneByType( type )
            obj = settings.value( "object" )
            if scene:
                scene.setObject( obj )
                self.addScene( scene )
        settings.endArray()

    # Scene methods
    def getTab(self):
        return self.mainWindow.tabWidget

    def getScene(self):
        tab = self.getTab()
        return tab.currentWidget()

    def newScene(self, type = 'moai'):
        scene = getSceneByType( type )
        if scene:
            obj = SceneObject()
            scene.setObject( obj )
            self.addScene( scene )
        return scene

    def addScene(self, scene):
        self._scenes += 1
        scene.setName( self._scenes )
        tab = self.getTab()
        tab.addTab( scene, scene.getName() )

    def openSceneSource(self):
        scene = self.getScene()
        if scene:
            scene.openSource()

    def reloadSceneSource(self):
        scene = self.getScene()
        if scene:
            scene.reload()

    def swapProjects(self, prevIndex, nextIndex):
        tab = self.getTab()
        if prevIndex >= 0:
            prevScene = tab.widget( prevIndex )
            if prevScene and prevScene is not None:
                prevScene.pause()

        self._currentIndex = nextIndex
        nextScene = tab.widget( nextIndex )
        if nextScene and nextScene is not None:
            nextScene.start()
            self.sceneSizeWidget.findSizeObj( nextScene.obj() )

    # Callbacks
    def onMenu(self, node):
        name = node.name
        print("SceneEditor onMenu: " + name )

        if name == 'new_scene_moai':
            self.newScene()
        elif name == 'open_scene':
            self.openSceneSource()
        elif name == 'reload_scene':
            self.reloadSceneSource()

    def onTool(self, node):
        name = node.name
        print("SceneEditor onTool: " + name )

    def onSceneChanged(self, index):
        self.swapProjects(self._currentIndex, index)

    def onSceneCloseRequested(self, index):
        tab = self.getTab()
        closeScene = tab.widget( index )
        closeScene.stop()

        tab.removeTab( index )

    def sceneChangeSize(self, size):
        scene = self.getScene()
        if scene:
            scene.resize( size['width'], size['height'] )
            scene.reload()
        print('Scene {} size changed: {} x {}'.format(scene.getName(), size['width'], size['height']))

##----------------------------------------------------------------##
class SceneEditorModule( SubEditorModule ):
    def getParentModuleId( self ):
        return 'scene_editor'

    def getSceneEditor( self ):
        return self.getParentModule()

    # def getSceneToolManager( self ):
    #     return self.getModule( 'scene_tool_manager' )

    # def changeSceneTool( self, toolId ):
    #     self.getSceneToolManager().changeTool( toolId )

    # def getAssetSelection( self ):
    #     return getSelectionManager( 'asset' ).getSelection()

##----------------------------------------------------------------##
def getSceneSelectionManager():
    return app.getModule('scene_editor').selectionManager

##----------------------------------------------------------------##
SceneEditor().register()
        