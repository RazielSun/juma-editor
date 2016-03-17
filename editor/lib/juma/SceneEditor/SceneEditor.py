#!/usr/bin/env python

import sys
import os

from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.qt.TopEditorModule    import TopEditorModule, QtMainWindow, SubEditorModule

##----------------------------------------------------------------##
class SceneEditor( TopEditorModule ):
    _name       = 'scene_editor'
    _dependency = [ 'qt', 'moai' ]

    def __init__(self):
        super(SceneEditor, self).__init__()
        self.runtime        = None

    def getWindowTitle( self ):
        return 'Scene Editor'

    def getSelectionGroup( self ):
        return 'scene'

    def getRuntime(self):
        if not self.runtime:
            self.runtime = self.affirmModule('moai')
        return self.runtime

    def onLoad( self ):
        self.mainWindow.setMenuWidget( self.getQtSupport().getSharedMenubar() )

        self.containers  = {}

        self.findMenu( 'main/edit' ).addChild([
            dict( name = 'reload_project', label = 'Reload Project', shortcut = 'ctrl+R' ),
        ], self )

        self.mainToolBar = self.addToolBar( 'editor', self.mainWindow.requestToolBar( 'main' ) )     

        self.addTool( 'editor/open_project', label = 'Open Project',
            menu_link = 'main/file/open_project', icon = 'tools/inbox' )
        
        self.addTool( 'editor/reload_project', label = 'Reload Project',
            menu_link = 'main/edit/reload_project', icon = 'tools/reload' )

        return True

    def onStart( self ):
        self.restoreWindowState( self.mainWindow )
        self.setFocus()

    def reloadProject(self):
        runtime = self.getRuntime()
        runtime.reset()

    # Callbacks
    def onMenu(self, node):
        name = node.name
        if name == 'reload_project':
            self.reloadProject()

    def onTool(self, node):
        name = node.name

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
        