#!/usr/bin/env python

import os.path
import time
import math
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                				import signals, app, jsonHelper, Field
from AssetEditor             				import AssetEditorModule
from MeshObject 							import MeshObject
from converters 							import PyAssimpConverter, AnimationConverter
from juma.qt.controls.GenericListWidget 	import GenericListWidget

from juma.qt.controls.PropertyEditor.PropertyEditor import buildFieldEditor

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
def _traceClass( clazz ):
	print(" TRACE: " + str(clazz))
	for it in clazz.__dict__.items():
		print(" - " + str(it))

##----------------------------------------------------------------##
class MeshExporter( AssetEditorModule ):
	"""docstring for MeshExporter"""
	_name = 'mesh_exporter'
	_dependency = [ 'qt', 'moai', 'asset_editor' ]

	def __init__(self):
		super(MeshExporter, self).__init__()
		self.config_name = "mesh_export_config"
		self.export_path = "assets/3ds/"
		self.objects = []
		self.config = {}

	def onLoad(self):
		self.window = self.requestDockWindow(
			'MeshExporter',
			title = 'Mesh Exporter',
			dock  = 'right',
			minSize = (300,200)
			)

		self.toolbar = self.addToolBar( 'mesh_exporter', self.window.addToolBar() )

		self.export_path_edit = epedit= QtGui.QLineEdit( None )
		epedit.textChanged.connect( self.onExportPathChange )

		self.addTool( 'mesh_exporter/add_object', label = 'Add', icon = 'plus_mint' )
		self.addTool( 'mesh_exporter/remove_object', label = 'Remove', icon = 'minus' )
		self.addTool( 'mesh_exporter/preview_render', label = 'Preview', icon = 'view' )
		self.addTool( 'mesh_exporter/export', label = 'Export', icon = 'diskette' )
		# self.addTool( 'mesh_exporter/export_all', label = 'ExportAll' )
		# self.addTool( 'mesh_exporter/export_animation', label = 'Export Animation Json', icon = 'diskette' )
		# self.addTool( 'mesh_exporter/play_animation', label = 'Play', icon = 'run' )
		self.addTool( 'mesh_exporter/export_path_edit', widget = epedit )

		self.mainWidget = wdgt = QtGui.QWidget()
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(wdgt.sizePolicy().hasHeightForWidth())
		wdgt.setSizePolicy(sizePolicy)
		wdgt.setMinimumSize(QtCore.QSize(300, 400))
		wdgt.resize(300, 500)

		self.mainLayout = layout = QtGui.QFormLayout(wdgt)
		layout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
		layout.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
		layout.setContentsMargins(5, 5, 5, 5)

		self.window.addWidget( wdgt, expanding=False )

		self.editors = {}

		self.addField( Field("SetPerPixel", "PerPixelSize", float) )
		self.addField( Field("SetTexture", "Texture", str) )
		self.addField( Field("SetBakeLight", "BakeLight", bool) )
		self.addField( Field("SetDiffusePower", "DiffusePower", float) )
		self.addField( Field("SetAmbientLight", "AmbientLight", 'color') )
		self.addField( Field("SetLightDirection", "LightDircetion", 'vec3') )
		self.addField( Field("SetStaticBatch", "StaticBatch", bool) )
		self.addField( Field("SetExportName", "ExportName", str) )
		self.addField( Field("SetExportAnimationName", "ExportAnimName", str) )
		self.addField( Field("SetExportMesh", "ExportMesh", bool) )
		self.addField( Field("SetExportAnimation", "ExportAnimation", bool) )
		self.addField( Field("SetExportTransform", "ExportTransform", bool) )
		self.addField( Field("SetExportBuffers", "ExportBuffers", bool) )

		self.list = self.window.addWidget( 
				MeshExporterListWidget( 
					multiple_selection = False,
					editable           = False,
					drag_mode          = False
				)
			)
		self.list.parentModule = self

		self.assimpConverter = PyAssimpConverter()

		signals.connect( 'project.load', 		self.onProjectLoad )

	def onUnload(self):
		self.saveConfig()

	def addField( self, field ):
		label = field.label
		editor  =  buildFieldEditor( self, field )
		labelWidget  = editor.initLabel( label, self.mainWidget )
		editorWidget = editor.initEditor( self.mainWidget )
		self.mainLayout.addRow ( labelWidget, editorWidget )
		self.editors[label] = editor
		return editor

	def updateList( self ):
		self.list.rebuild()

	def getObjects( self ):
		return self.objects

	def getObjectData( self ):
		data = []
		for obj in self.objects:
			data.append( obj.GetSaveObject() )
		return data

	def openObject( self ):
		fileName, filt = self.getSceneEditor().openFile( "3D Object (*.fbx *.obj)", "Open 3D Object" )
		if fileName:
			self.addObject( fileName )
			self.saveConfig()

	def addObject( self, data ):
		obj = None
		if type(data) is dict:
			obj = MeshObject( data )
		else:
			obj = MeshObject( app.getRelPath(data) )
		self.objects.append(obj)
		self.onAddObject( obj )

	def getObjectIndex( self, obj ):
		index = -1
		for i, o in enumerate(self.objects):
			if o == obj:
				index = i
				break
		return index

	def removeObjects( self ):
		selection = self.list.getSelection()
		for obj in selection:
			index = self.getObjectIndex( obj )
			if index >= 0:
				self.objects.pop( index )
				self.onRemoveObject( obj )
		self.saveConfig()

	def saveConfig( self ):
		self.config["export_path"] = self.export_path
		self.config["data"] = self.getObjectData()

		proj = self.getProject()
		if proj:
			proj.setConfig( self.config_name, self.config )
			proj.saveConfig()

	def loadConfig( self ):
		data = self.config.get( "data", None )
		if data:
			self.objects = []
			for p in data:
				self.addObject( p )
		self.export_path = self.config.get("export_path", "")
		self.export_path_edit.setText( self.export_path )

	def getFullPath( self, path ):
		project = app.getProject()
		if project:
			path = project.getPath(path)
		return path

	##----------------------------------------------------------------##
	def previewRender( self, options = None ):
		signals.emitNow( 'mesh.preview' )
		selection = self.list.getSelection()
		self.assimpConverter.preview(selection, options)

	def playAnimation( self ):
		self.previewRender()
		self.exportAnimationSelected()

		path = self.getFullPath(self.export_path)
		selection = self.list.getSelection()
		for obj in selection:
			signals.emitNow( 'mesh.animation_play', path + obj.GetExportAnimation() )

	##----------------------------------------------------------------##
	def export( self, olist, options = None ):
		path = self.getFullPath(self.export_path)
		self.assimpConverter.export(olist, path, options)

	def exportSelected( self ):
		selection = self.list.getSelection()
		self.export( selection )

	def exportAnimation( self, olist ):
		print("Export Animation ERROR! FIXME!")
		# for obj in olist:
		# 	self.fbxConvert( obj )

	def exportAnimationSelected( self ):
		selection = self.list.getSelection()
		self.exportAnimation( selection )

	def exportAll( self ):
		self.export( self.objects )

	##----------------------------------------------------------------##
	def onMenu(self, node):
		name = node.name

	def onTool( self, tool ):
		name = tool.name

		if name == 'add_object':
			self.openObject()
		elif name == 'remove_object':
			self.removeObjects()

		elif name == 'preview_render':
			self.previewRender()
		elif name == 'export':
			self.exportSelected()
			self.exportAnimationSelected()
		elif name == 'play_animation':
			self.playAnimation()
		elif name == 'export_all':
			self.exportAll()

	def onAddObject( self, obj ):
		self.list.addNode( obj )

	def onRemoveObject( self, obj ):
		self.list.removeNode( obj )

	def onProjectLoad( self, project ):
		self.config = project.getConfig( self.config_name, None )
		if self.config is None:
			self.config = {}
			self.saveConfig()
		else:
			self.loadConfig()
		self.updateList()

	def onExportPathChange( self, text ):
		self.export_path = text

	def onPropertyChanged( self, field, value ):
		selection = self.list.getSelection()
		for obj in selection:
			fname = field.model
			func = getattr(obj, fname)
			func( value )

	def onItemSelectionChanged( self ):
		selection = self.list.getSelection()
		for obj in selection:
			self.editors.get("PerPixelSize").set( obj.GetPerPixel() )
			self.editors.get("Texture").set( obj.GetTexture() )
			self.editors.get("BakeLight").set( obj.GetBakeLight() )
			self.editors.get("DiffusePower").set( obj.GetDiffusePower() )
			self.editors.get("AmbientLight").set( obj.GetAmbientLight() )
			self.editors.get("LightDircetion").set( obj.GetLightDirection() )
			self.editors.get("StaticBatch").set( obj.GetStaticBatch() )
			self.editors.get("ExportName").set( obj.GetExportName() )
			self.editors.get("ExportAnimName").set( obj.GetExportAnimation() )
			self.editors.get("ExportMesh").set( obj.GetExportMesh() )
			self.editors.get("ExportAnimation").set( obj.GetExportAnimation() )
			self.editors.get("ExportTransform").set( obj.GetExportTransform() )
			self.editors.get("ExportBuffers").set( obj.GetExportBuffers() )
	
##----------------------------------------------------------------##

MeshExporter().register()

##----------------------------------------------------------------##
class MeshExporterListWidget( GenericListWidget ):
	def getNodes( self ):
		return self.parentModule.getObjects()

	def updateItemContent( self, item, node, **options ):
		item.setText( repr(node) )

	def onItemSelectionChanged(self):
		self.parentModule.onItemSelectionChanged()
