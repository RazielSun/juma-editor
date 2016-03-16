#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.qt.TopEditorModule    import TopEditorModule, QtMainWindow, SubEditorModule

from LayoutView                  import LayoutView

##----------------------------------------------------------------##
class SceneEditor( TopEditorModule ):
    _name       = 'scene_editor'
    _dependency = [ 'qt', 'moai' ]

    def __init__(self):
        super(SceneEditor, self).__init__()
        self.runtime        = None

    def getWindowTitle( self ):
        return 'Scene Editor'

    def getRuntime(self):
        if not self.runtime:
            self.runtime = self.affirmModule('moai')
        return self.runtime

    def onLoad( self ):
        self.mainWindow.setMenuWidget( self.getQtSupport().getSharedMenubar() )

        self.getTab().currentChanged.connect(self.onTabChanged)
        self.getTab().tabCloseRequested.connect(self.onTabCloseRequested)

        self.containers  = {}

        self.findMenu( 'main/edit' ).addChild([
            dict( name = 'reload_project', label = 'Reload Project', shortcut = 'ctrl+R' ),
        ], self )

        self.findMenu( 'main/layout' ).addChild([
            dict( name = 'new_layout', label = 'New Layout' ),
        ], self )

        self.mainToolBar = self.addToolBar( 'editor', self.mainWindow.requestToolBar( 'main' ) )     

        self.addTool( 'editor/open_project', label = 'Open Project',
            menu_link = 'main/file/open_project', icon = 'tools/folder' )
        
        self.addTool( 'editor/reload_project', label = 'Reload Project',
            menu_link = 'main/edit/reload_project', icon = 'tools/reload' )

        return True

    def onStart( self ):
        self.setFocus()
        self.restoreWindowState( self.mainWindow )

    # Save and Restore States
    def saveWindowState( self, window ):
        super(SceneEditor, self).saveWindowState( window )
        # settings = self.getQtSettingObject()
        # tab = self.getTab()
        # settings.beginWriteArray(self.getName() + '_tab_widgets')
        # for i in range(tab.count()):
        #     settings.setArrayIndex(i)
        #     scene = tab.widget(i)
        #     settings.setValue( "type", scene.project().getType() )
        #     obj_ = scene.head()
        #     settings.setValue( "object", obj_ )
        # settings.endArray()

    def restoreWindowState( self, window ):
        super(SceneEditor, self).restoreWindowState( window )
        # settings = self.getQtSettingObject()
        # size = settings.beginReadArray(self.getName() + '_tab_widgets')
        # for i in range(size):
        #     settings.setArrayIndex(i)
        #     type = settings.value( "type" )
        #     scene = getSceneByType( type )
        #     obj = settings.value( "object" )
        #     if scene:
        #         scene.setHeader( obj )
        #         self.addScene( scene )
        # settings.endArray()

    # Scene methods
    def getTab(self):
        return self.mainWindow.centerTabWidget

    def newLayout(self):
        layout = LayoutView()
        tab = self.getTab()
        tab.addTab( layout, "moai.layout *" )
        tab.setCurrentIndex( tab.count()-1 )

    def reloadProject(self):
        runtime = self.getRuntime()
        runtime.reset()

    # Callbacks
    def onMenu(self, node):
        name = node.name
        if name == 'reload_project':
            self.reloadProject()

        if name == 'new_layout':
            self.newLayout()
        # if name == 'new_scene':
        #     self.newScene()
        # elif name == 'open_file':
        #     self.openSceneSource()
        # elif name == 'open_scene':
        #     self.openSceneSource()
        # elif name == 'reload_scene':
        #     self.reloadSceneSource()

    def onTool(self, node):
        name = node.name

    def onTabChanged(self, index):
        pass

    def onTabCloseRequested(self, index):
        tab = self.getTab()
    #     closeScene = tab.widget( index )
    #     closeScene.stop()
        tab.removeTab( index )

    

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
        