#!/usr/bin/env python

import os.path
import time
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                	import signals, app
from AssetEditor             	import AssetEditorModule
from MeshNodes 					import OBJNode
from juma.qt.controls.GenericListWidget import GenericListWidget

##----------------------------------------------------------------##
_gInstalledFBX = False

try:
	from fbx import *
	import FbxCommon
	import fbxsip
	_gInstalledFBX = True
except ImportError:
	print("MeshExporter import error: Did you install FBX SDK?")

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class MeshObject( object ):
	def __init__( self, path, per_pixel = 256 ):
		self.fullpath = path
		name = os.path.basename( path )
		self.name = name.lower()
		frm = self.name.split('.')[-1]
		self.format = frm.upper()
		self._per_pixel = per_pixel

	def __repr__( self ):
		return "< {} >   {}".format(self.format, self.name)

	def getPath( self ):
		return self.fullpath

	def getFormat( self ):
		return self.format

	def getPerPixel( self ):
		return self._per_pixel

	def setPerPixel( self, per_pixel ):
		self._per_pixel = per_pixel

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

		self.per_pixel_edit = ppedit = QtGui.QLineEdit( None )
		ppedit.setMaximumSize( 50, 20 )
		# intValidator = QtGui.QIntValidator()
		# ppedit.setValidator( intValidator )
		ppedit.textChanged.connect( self.onPerPixelChange )

		self.export_path_edit = epedit= QtGui.QLineEdit( None )
		epedit.textChanged.connect( self.onExportPathChange )

		self.addTool( 'mesh_exporter/add_object', label = 'Add', icon = 'plus_mint' )
		self.addTool( 'mesh_exporter/remove_object', label = 'Remove', icon = 'minus' )
		self.addTool( 'mesh_exporter/preview_render', label = 'Preview' )
		self.addTool( 'mesh_exporter/per_pixel_edit', widget = ppedit )
		self.addTool( 'mesh_exporter/export_path_edit', widget = epedit )
		self.addTool( 'mesh_exporter/export', label = 'Export' )
		self.addTool( 'mesh_exporter/export_all', label = 'ExportAll' )

		self.list = self.window.addWidget( 
				MeshExporterListWidget( 
					multiple_selection = False,
					editable           = False,
					drag_mode          = False
				)
			)
		self.list.parentModule = self

		signals.connect( 'project.load', 		self.onProjectLoad )

	def onUnload(self):
		self.saveConfig()

	def updateList( self ):
		self.list.rebuild()

	def getObjects( self ):
		return self.objects

	def getObjectData( self ):
		data = []
		for obj in self.objects:
			dct = dict(path = obj.getPath(), per_pixel = obj.getPerPixel())
			data.append( dct )
		return data

	def openObject( self ):
		fileName, filt = self.getSceneEditor().openFile( "3D Object (*.fbx *.obj)", "Open 3D Object" )
		if fileName:
			self.addObject( fileName )
			self.saveConfig()

	def addObject( self, data ):
		obj = None
		if type(data) is dict:
			obj = MeshObject( data.get('path'), data.get('per_pixel') )
		else:
			obj = MeshObject( data )
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

	##----------------------------------------------------------------##
	def previewRender( self ):
		signals.emitNow( 'mesh.preview' )
		selection = self.list.getSelection()
		for obj in selection:
			node = self.getNodeFromObject( obj )
			signals.emitNow( 'mesh.render', node, obj )

	def export( self, objlist ):
		signals.emitNow( 'mesh.clear' )
		for obj in objlist:
			node = self.getNodeFromObject( obj )
			signals.emitNow( 'mesh.create', node, obj )
		signals.emitNow( 'mesh.save_by', self.export_path )

	def exportSelected( self ):
		selection = self.list.getSelection()
		self.export( selection )

	def exportAll( self ):
		self.export( self.objects )

	def getNodeFromObject( self, obj ):
		node = None
		frm = obj.getFormat()
		if frm == 'FBX':
			node = self.getFBXNode( obj.getPath() )
		elif frm == 'OBJ':
			node = self.getOBJNode( obj.getPath() )
		return node

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

	def onPerPixelChange( self, text ):
		selection = self.list.getSelection()
		if text and text != '' and text != ' ':
			per_pixel = float(text)
			for obj in selection:
				obj.setPerPixel( per_pixel )

	def onExportPathChange( self, text ):
		self.export_path = text

	def onItemSelectionChanged( self ):
		selection = self.list.getSelection()
		for obj in selection:
			pp = "%d" % obj.getPerPixel()
			self.per_pixel_edit.setText( pp )

	##----------------------------------------------------------------##
	def getFBXNode( self, fileName ):
		if _gInstalledFBX:
			# Prepare the FBX SDK.
			lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
			# Open FBX file
			lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)
			if lResult:
				rootNode = lScene.GetRootNode()
				rootNode.FbxLayerElement = FbxLayerElement
				return rootNode
		return None
	# 	# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + 'output.fbx')

	# 	# Destroy all objects created by the FBX SDK.
	# 	# lSdkManager.Destroy()

	def getOBJNode( self, fileName ):
		node = OBJNode( fileName )
		return node

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
