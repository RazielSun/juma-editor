#!/usr/bin/env python

import sys
import os

# from PySide import QtCore, QtGui

from juma.core import app, signals
from juma.qt.TopEditorModule    import TopEditorModule, QtMainWindow, SubEditorModule

##----------------------------------------------------------------##
class MainEditor( TopEditorModule ):
    _name       = 'main_editor'
    _dependency = [ 'qt', 'moai' ]

    def __init__(self):
        super(MainEditor, self).__init__()
        self.runtime        = None

    def getWindowTitle( self ):
        return 'Main Editor'

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

        self.findMenu('main/window').addChild([
            'Game Preview',
            'Hierarchy',
            'Introspector',
            'Command History View',
            'Stats Viewer',
            'Debug Draw',
            'Run String Dock',
            '----',
            ]
        )

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
    def onMenu(self, menu):
        name = menu.name
        if name == 'reload_project':
            self.reloadProject()

        elif name == 'game_preview':
            self.getModule('game_preview').show()
        elif name == 'hierarchy':
            self.getModule('graph_editor').show()
        elif name == 'introspector':
            self.getModule('introspector').show()
        elif name == 'command_history_view':
            self.getModule('command_history_view').show()
        elif name == 'stats_viewer':
            self.getModule('stats_viewer').show()
        elif name == 'run_string_dock':
            self.getModule('run_string_dock').show()
        elif name == 'debug_draw':
            self.getModule('debug_draw_dock').show()


    def onTool(self, tool):
        name = tool.name

##----------------------------------------------------------------##
class MainEditorModule( SubEditorModule ):
    def getParentModuleId( self ):
        return 'main_editor'

    def getSceneEditor( self ):
        return self.getParentModule()

    def getSceneToolManager( self ):
        return self.getModule( 'scene_tool_manager' )

    def changeSceneTool( self, toolId ):
        self.getSceneToolManager().changeTool( toolId )

    # def getAssetSelection( self ):
    #     return getSelectionManager( 'asset' ).getSelection()

##----------------------------------------------------------------##
def getSceneSelectionManager():
    return app.getModule('main_editor').selectionManager

##----------------------------------------------------------------##

MainEditor().register()
        