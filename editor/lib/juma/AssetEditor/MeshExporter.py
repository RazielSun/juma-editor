#!/usr/bin/env python

import os.path
import time
import math
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                	import signals, app
from AssetEditor             	import AssetEditorModule
from MeshNodes 					import OBJNode
from juma.qt.controls.GenericListWidget import GenericListWidget

import pyassimp
from pyassimp.postprocess import *
# from pyassimp.helper import *

from fbx import *
import FbxCommon
import fbxsip

from ui.export_params_ui import Ui_ExportParams

##----------------------------------------------------------------##
def _getModulePath( path ):
	return os.path.dirname( __file__ ) + '/' + path

##----------------------------------------------------------------##
class MeshObject( object ):
	def __init__( self, path, per_pixel = 256.0, texture = "" ):
		self.SetPath( path )

		name = os.path.basename( path )
		array = name.split('.')
		self.format = array[-1].upper()
		self.name = array[0].lower()

		self._per_pixel = per_pixel
		self._texture = texture

	def __repr__( self ):
		return "< {} >   {}".format(self.format, self.name)

	def GetName( self ):
		return self.name

	def SetPath( self, path ):
		self.fullpath = app.getRelPath( path )

	def GetPath( self, abs_path = False ):
		if abs_path:
			return app.getAbsPath( self.fullpath )
		return self.fullpath

	def GetFormat( self ):
		return self.format

	def GetPerPixel( self ):
		return self._per_pixel

	def GetPerPixelStr( self ):
		return "%.1f" % self._per_pixel

	def SetPerPixel( self, per_pixel ):
		self._per_pixel = per_pixel

	def GetTexture( self, abs_path = False ):
		if abs_path:
			return app.getAbsPath( self._texture )
		return self._texture

	def SetTexture( self, texture ):
		self._texture = texture

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
		self.addTool( 'mesh_exporter/preview_render', label = 'Preview' )
		self.addTool( 'mesh_exporter/export', label = 'Export' )
		self.addTool( 'mesh_exporter/export_all', label = 'ExportAll' )
		self.addTool( 'mesh_exporter/export_path_edit', widget = epedit )

		container = QtGui.QWidget()
		self.ui = ui = Ui_ExportParams()
		ui.setupUi( container )
		self.window.addWidget( container, expanding=False )

		ui.perPixelEdit.textChanged.connect( self.onPerPixelChange )
		ui.textureEdit.textChanged.connect( self.onTextureChange )

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
			dct = dict(path = obj.GetPath(), per_pixel = obj.GetPerPixel(), texture = obj.GetTexture())
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
			obj = MeshObject( data.get('path'), data.get('per_pixel'), data.get('texture') )
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

	##----------------------------------------------------------------##
	def previewRender( self ):
		signals.emitNow( 'mesh.preview' )
		signals.emitNow( 'mesh.assimp_clear' )
		selection = self.list.getSelection()
		for obj in selection:
			self.convert3dScene( obj )
			# node = self.getNodeFromObject( obj )
			# signals.emitNow( 'mesh.render', node, obj )
		signals.emitNow( 'mesh.assimp_render' )

	def export( self, objlist ):
		# signals.emitNow( 'mesh.clear' )
		signals.emitNow( 'mesh.assimp_clear' )
		for obj in objlist:
			self.convert3dScene( obj )
			# node = self.getNodeFromObject( obj )
			# signals.emitNow( 'mesh.create', node, obj )
		# signals.emitNow( 'mesh.save_by', self.export_path )
		signals.emitNow( 'mesh.assimp_save', self.export_path )

	def exportSelected( self ):
		selection = self.list.getSelection()
		self.export( selection )

	def exportAll( self ):
		self.export( self.objects )

	def getNodeFromObject( self, obj ):
		node = None
		frm = obj.GetFormat()
		if frm == 'FBX':
			node = self.getFBXNode( obj.GetPath( True ) )
		elif frm == 'OBJ':
			node = self.getOBJNode( obj.GetPath( True ) )

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
		if text and text != '' and text != ' ':
			per_pixel = float(text)
			selection = self.list.getSelection()
			for obj in selection:
				obj.SetPerPixel( per_pixel )

	def onTextureChange( self, text ):
		if text:
			text = text.strip()
			selection = self.list.getSelection()
			for obj in selection:
				obj.SetTexture( text )

	def onExportPathChange( self, text ):
		self.export_path = text

	def onItemSelectionChanged( self ):
		selection = self.list.getSelection()
		for obj in selection:
			self.ui.perPixelEdit.setText( obj.GetPerPixelStr() )
			self.ui.textureEdit.setText( obj.GetTexture() )

	##----------------------------------------------------------------##
	def getFBXNode( self, fileName ):
		# Prepare the FBX SDK.
		lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
		# Open FBX file
		lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)
		if lResult:
			rootNode = lScene.GetRootNode()
			rootNode.FbxLayerElement = FbxLayerElement
			return rootNode
		# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + 'output.fbx')

		# Destroy all objects created by the FBX SDK.
		lSdkManager.Destroy()

	def getOBJNode( self, fileName ):
		node = OBJNode( fileName )
		return node

	def getTransform( self, nodeTr, rootTr ):
		if not rootTr:
			return nodeTr
		newTr = []
		for i, row in enumerate(nodeTr):
			newTr.append([])
			for j, col in enumerate(row):
				newTr[i].append(0)
				for k in range(0,4):
					newTr[i][j] += rootTr[i][k] * nodeTr[k][j]
		return newTr

	def quatToEuler( self, q ):
		a = math.atan2(2*(q.w*q.x+q.y*q.z), 1-2*(q.x*q.x+q.y*q.y))
		b = math.asin(2*(q.w*q.y-q.z*q.x))
		c = math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z))
		return a, b, c

	def recur_node(self,node,data,tr = None,level = 0):
		print("  " + "\t" * level + "- " + str(node))

		hasMesh = None
		for mesh in node.meshes:
			hasMesh = mesh.name
			print("  " + "\t" * level + " mesh:" + str(mesh.name))

		ntr = self.getTransform(node.transformation, tr)

		if hasMesh:
			m = pyassimp.matrix_from_transformation(ntr)
			scl, rot, pos = pyassimp.decompose_matrix(m)
			ra, rb, rc = self.quatToEuler(rot)
			trDict = {
				'name': hasMesh,
				'pos':[pos.x, pos.y, pos.z],
				'rot':[math.degrees(ra), math.degrees(rb), math.degrees(rc)],
				'scl':[scl.x, scl.y, scl.z],
			}
			data.append( trDict )
			# print("  " + "\t" * level + " pos {} {} {}".format(pos.x, pos.y, pos.z))
			# print("  " + "\t" * level + " rot {} {} {}".format(a, b, c))
			# print("  " + "\t" * level + " scl {} {} {}".format(scl.x, scl.y, scl.z))

		for child in node.children:
			self.recur_node(child,data,ntr,level+1)

	def convert3dScene(self, obj):
	    scene = pyassimp.load(obj.GetPath( True ), processing = (aiProcessPreset_TargetRealtime_MaxQuality|aiProcess_FlipUVs))
	    #the model we load
	    print
	    print("MODEL:" + str(obj))
	    print
	    
	    #write some statistics
	    print("SCENE:")
	    print("  meshes:" + str(len(scene.meshes)))
	    print("  materials:" + str(len(scene.materials)))
	    print("  textures:" + str(len(scene.textures)))
	    print
	    
	    print("MESHES:")
	    for index, mesh in enumerate(scene.meshes):
	    	if not mesh.name:
	    		mesh.name = "{}Mesh{}".format(obj.GetName(),index+1)
	        print("  MESH id: " + str(index+1) + " (" + str(mesh.name) + ")")
	        print("    material id: " + str(mesh.materialindex+1))
	        print("    vertices: " + str(len(mesh.vertices)))
	        print("    normals: " + str(len(mesh.normals)))
	        print("    colors: " + str(len(mesh.colors)))
	        print("    uv channels: " + str(len(mesh.texturecoords)))
	        print("    uv-component-count:" + str(len(mesh.numuvcomponents)))
	        print("    faces:" + str(len(mesh.faces)))
	        print("    bones:" + str(len(mesh.bones)))
	        print
	        meshDict = {
	            'name'          : mesh.name or index,
	            'vertices'      : mesh.vertices,
	            'verticesCount' : len(mesh.vertices),
	            'texturecoords' : mesh.texturecoords,
	            'faces'         : mesh.faces,
	            'facesCount'    : len(mesh.faces),
	            'bones'         : mesh.bones,
	            'normals'       : mesh.normals
	        }
	        signals.emitNow( 'mesh.assimp_mesh', meshDict, obj )

	    print
	    print("NODES:")
	    transforms = []
	    self.recur_node(scene.rootnode, transforms)
	    size = obj.GetPerPixel()
	    for tr in transforms:
	    	pos = tr['pos']
	    	for i, v in enumerate(pos):
	    		pos[i] = v * size
	    signals.emitNow( 'mesh.assimp_transforms', obj.GetName(), transforms )

	    print("MATERIALS:")
	    for index, material in enumerate(scene.materials):
	        print("  MATERIAL (id:" + str(index+1) + ")")
	        for key, value in material.properties.items():
	            print("    %s: %s" % (key, value))
	    print
	    
	    print("TEXTURES:")
	    for index, texture in enumerate(scene.textures):
	        print("  TEXTURE" + str(index+1))
	        print("    width:" + str(texture.width))
	        print("    height:" + str(texture.height))
	        print("    hint:" + str(texture.achformathint))
	        print("    data (size):" + str(len(texture.data)))
	    
	    # Finally release the model
	    pyassimp.release(scene)

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
