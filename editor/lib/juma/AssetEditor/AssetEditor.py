#!/usr/bin/env python

import sys
import os

from PySide                     import QtCore, QtGui
from PySide.QtGui               import QFileDialog

from juma.core import app, signals
from juma.qt.TopEditorModule    import TopEditorModule, QtMainWindow, SubEditorModule

##----------------------------------------------------------------##
class AssetEditor( TopEditorModule ):
    _name       = 'asset_editor'
    _dependency = [ 'qt', 'moai' ]

    def __init__(self):
        super(AssetEditor, self).__init__()
        self.runtime        = None

    def getWindowTitle( self ):
        return 'Asset Editor'

    def getRuntime(self):
        if not self.runtime:
            self.runtime = self.affirmModule('moai')
        return self.runtime

    def onLoad( self ):
    	self.mainWindow.setMenuWidget( self.getQtSupport().getSharedMenubar() )

    	self.findMenu( 'main/asset' ).addChild([
            dict( name = 'refresh_assets', label = 'Refresh Assets', shortcut = 'ctrl+G' ),
        ], self )

    	self.findMenu('main/window').addChild([
            'Mesh Exporter',
            'Mesh Preview',
            '----',
            ],
        self )

    	return True

    ##----------------------------------------------------------------##
    def openFile( self, fileformat, title, folder = None ):
        if folder is None:
            if self.getProject().getPath():
                folder = self.getProject().getPath()
            else:
                folder = '~'
        return QFileDialog.getOpenFileName(self.getMainWindow(), title, folder, fileformat)

    ##----------------------------------------------------------------##
    def onMenu(self, node):
        name = node.name

        if name == 'mesh_exporter':
            self.getModule('mesh_exporter').show()
        elif name == 'mesh_preview':
            self.getModule('mesh_preview').show()

        elif name == 'refresh_assets':
            self.getProject().assetLibrary.clearAssets()
            runtime = self.getRuntime()
            runtime.refreshAssets()

##----------------------------------------------------------------##
class AssetEditorModule( SubEditorModule ):
    def getParentModuleId( self ):
        return 'asset_editor'

    def getSceneEditor( self ):
        return self.getParentModule()

##----------------------------------------------------------------##

AssetEditor().register()
        