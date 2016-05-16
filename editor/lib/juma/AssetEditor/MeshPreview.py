#!/usr/bin/env python

import os.path

from PySide  		import QtCore, QtGui, QtOpenGL
from PySide.QtGui 	import QFileDialog

from juma.core 					import signals, app
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas
from AssetEditor             	import AssetEditorModule
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class MeshPreview( AssetEditorModule ):
	_name       = 'mesh_preview'
	_dependency = [ 'qt', 'moai', 'asset_editor', 'mesh_exporter' ]

	def __init__(self):
		super( MeshPreview, self ).__init__()

	def onLoad(self):
		self.window = window = self.requestDocumentWindow( title = 'Mesh Preview' )

		self.canvas = canvas = window.addWidget(
				MeshPreviewCanvas(
					context_prefix = 'preview_canvas'
				)
			)

		canvas.loadScript( _getModulePath('MeshExporter.lua') )

		# SIGNALS
		signals.connect( 'mesh.preview',   	self.onShowPreview )
		signals.connect( 'mesh.render',   	self.onMeshRender )
		signals.connect( 'mesh.clear',   	self.onClear )
		signals.connect( 'mesh.create',   	self.onMeshCreate )
		signals.connect( 'mesh.save_by',   	self.onMeshSaveBy )

	def onSetFocus( self ):
		self.getModule( 'asset_editor' ).setFocus()
		self.window.show()
		self.window.setFocus()

	def onUpdateTimer( self ):
		canvas = self.canvas
		if canvas:
			canvas.updateCanvas( no_sim = False, forced = True )

	##----------------------------------------------------------------##
	def onShowPreview( self ):
		self.show()

	def onMeshRender( self, node, obj ):
		canvas = self.canvas
		if canvas:
			canvas.safeCallMethod( "view", "renderNode", node, obj )

	def onClear( self ):
		canvas = self.canvas
		if canvas:
			canvas.safeCallMethod( "view", "clearModels" )

	def onMeshCreate( self, node, obj ):
		canvas = self.canvas
		if canvas:
			canvas.safeCallMethod( "view", "createModel", node, obj )

	def onMeshSaveBy( self, path ):
		canvas = self.canvas
		if canvas:
			canvas.safeCallMethod( "view", "saveBy", path )

##----------------------------------------------------------------##

MeshPreview().register()

##----------------------------------------------------------------##
class MeshPreviewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( MeshPreviewCanvas, self ).__init__( *args, **kwargs )
