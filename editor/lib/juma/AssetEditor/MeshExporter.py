#!/usr/bin/env python

import os.path
import time
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                	import signals, app
from AssetEditor             	import AssetEditorModule
from juma.moai.MOAIEditCanvas 	import MOAIEditCanvas
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
	def __init__( self, path ):
		self.fullpath = path
		self.name = os.path.basename( path )
		self.format = self.name.split('.')[-1]

	def __repr__( self ):
		return "< {} >   {}".format(self.format, self.name)

	def getPath( self ):
		return self.fullpath

	def getFormat( self ):
		return self.format

##----------------------------------------------------------------##
class MeshExporter( AssetEditorModule ):
	"""docstring for MeshExporter"""
	_name = 'mesh_exporter'
	_dependency = [ 'qt', 'moai', 'asset_editor' ]

	def __init__(self):
		super(MeshExporter, self).__init__()
		self.config_name = "mesh_export_config"
		self.export_path = "assets/3ds/"
		self.pixel_per_point = 256
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

		self.addTool( 'mesh_exporter/add_object', label = 'Add', icon = 'plus_mint' )
		self.addTool( 'mesh_exporter/remove_object', label = 'Remove', icon = 'minus' )
		self.addTool( 'mesh_exporter/preview_render', label = 'Preview' )
		self.addTool( 'mesh_exporter/export', label = 'Export' )

		self.list = self.window.addWidget( 
				MeshExporterListWidget( 
					multiple_selection = False,
					editable           = False,
					drag_mode          = False
				)
			)
		self.list.parentModule = self

		self.canvas = canvas = self.window.addWidget(
				MeshPreviewCanvas(
					context_prefix = 'preview_canvas'
				)
			)

		canvas.loadScript( _getModulePath('MeshExporter.lua') )

		signals.connect( 'project.load', 		self.onProjectLoad )

	def updateList( self ):
		self.list.rebuild()

	def getObjects( self ):
		return self.objects

	def getObjectPaths( self ):
		paths = []
		for obj in self.objects:
			paths.append( obj.getPath() )
		return paths

	def openObject( self ):
		fileName, filt = self.getSceneEditor().openFile( "3D Object (*.fbx *.obj)", "Open 3D Object" )
		if fileName:
			self.addObject( fileName )
			self.saveConfig()

	def addObject( self, fileName ):
		obj = MeshObject( fileName )
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
		self.config["pixel_per_point"] = self.pixel_per_point
		self.config["paths"] = self.getObjectPaths()

		proj = self.getProject()
		if proj:
			proj.setConfig( self.config_name, self.config )
			proj.saveConfig()

	def loadConfig( self ):
		paths = self.config.get( "paths", None )
		if paths:
			self.objects = []
			for p in paths:
				self.addObject( p )

	##----------------------------------------------------------------##
	def previewRender( self ):
		selection = self.list.getSelection()
		canvas = self.canvas
		if canvas:
			for obj in selection:
				node = self.getNodeFromObject( obj )
				canvas.safeCallMethod( "view", "renderNode", node, obj.getFormat(), self.pixel_per_point )

	def exportAll( self ):
		pass

	def getNodeFromObject( self, obj ):
		node = None
		frm = obj.getFormat()
		if frm == 'fbx':
			node = self.getFBXNode( obj.getPath() )
		elif frm == 'obj':
			pass
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

	def onUpdateTimer( self ):
		canvas = self.canvas
		if canvas:
			canvas.updateCanvas( no_sim = False, forced = True )

	##----------------------------------------------------------------##
	def getFBXNode( self, fileName ):
		if _gInstalledFBX:
			# Prepare the FBX SDK.
			lSdkManager, lScene = FbxCommon.InitializeSdkObjects()
			# Open FBX file
			lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)
			if lResult:
				return lScene.GetRootNode()
		return None

	# 	self.parseFBXScene( lScene, fileName )

	# 	# ListAllMeshesCount( lScene )
	# 	# TraceAllMeshes( lScene )

	# 	# newName = 
	# 	# path = os.path.dirname( fileName )
	# 	# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + 'output.fbx')

	# 	# Destroy all objects created by the FBX SDK.
	# 	# lSdkManager.Destroy()

	# def parseFBXScene( self, scene, fileName ):
	# 	runtime = self.getRuntime()
	# 	rootNode = scene.GetRootNode()
	# 	for i in range(rootNode.GetChildCount()):
	# 		child = rootNode.GetChild(i)
	# 		mesh = child.GetMesh()
	# 		if mesh:
	# 			meshLua = runtime.getNewMeshExporter()
	# 			meshLua.setNode( meshLua, child )
	# 			meshLua.createMOAIMesh( meshLua )
	# 			path = os.path.dirname(fileName)
	# 			meshLua.save( meshLua, path )
		

##----------------------------------------------------------------##

MeshExporter().register()

##----------------------------------------------------------------##
class MeshExporterListWidget( GenericListWidget ):
	def getNodes( self ):
		return self.parentModule.getObjects()

	def updateItemContent( self, item, node, **options ):
		item.setText( repr(node) )

##----------------------------------------------------------------##
class MeshPreviewCanvas( MOAIEditCanvas ):
	def __init__( self, *args, **kwargs ):
		super( MeshPreviewCanvas, self ).__init__( *args, **kwargs )

##----------------------------------------------------------------##
class OBJNode( object ):
	def __init__( self, path ):
		self.fullpath = path


def ListAllMeshesCount(pScene):
	print("NUMBER OF GEOMETRIES :: %i" % pScene.GetGeometryCount())

# lNode = pScene.GetRootNode()
# if lNode:
# 		for i in range(lNode.GetChildCount()):
# 			lChildNode = lNode.GetChild(i)
# print("CHILD:", lChildNode.GetName())
# 			print("CHILD MESH:", lChildNode.GetMesh())
# lPoly = lMesh.GetPolygonCount()
# print("MESH POLYGONS :: %i" % lPoly)
# print("MESH VertexCount :: %i" % lMesh.GetPolygonVertexCount())
# print("MESH Layers :: %i" % lMesh.GetLayerCount())
					# layer = lMesh.GetLayer(0)
					# uvElem = layer.GetUVs()
					# uvElemD = uvElem.GetDirectArray()
					# uvElemI = uvElem.GetIndexArray()

					# controlPoints = lMesh.GetControlPoints()
					# for p in range(lPoly):
					# 	pSize = lMesh.GetPolygonSize(p)
					# 	for v in range(pSize):
					# 		vertexIndex = lMesh.GetPolygonVertex(p, v)
					# 		uvIndex = lMesh.GetTextureUVIndex(p, v)
					# 		print("   VERTEX {} ||| pos: {} || uv: {} index {}".format(
					# 			vertexIndex, 0 
					# 			controlPoints[vertexIndex], fbx.FbxVector4(0.500000, 0.500000, 0.500000, 0.000000)
					# 			uvElemD.GetAt(uvIndex), fbx.FbxVector2(0.000000, 1.000000)
					# 			uvElemI.GetAt(uvIndex), 0
					# 			))
					# for materialIndex in range( 0, lChildNode.GetMaterialCount() ):
					# 	material = lChildNode.GetMaterial( materialIndex )
					# 	print(" material:", material, material.GetName())
					# 	for propertyIndex in range( 0, FbxLayerElement.sTypeTextureCount() ):
					# 		property = material.FindProperty( FbxLayerElement.sTextureChannelNames( propertyIndex ) )
					# 		print("  property:", property, property.GetName())
					# 		texture = property.GetSrcObject()
					# 		print("   texture:", texture)
					# 		if texture:
					# 			textureFilename = texture.GetFileName()
					# 			print("   ", texture.GetName())
					# 			print("   filename:", textureFilename)

def TraceAllMeshes(pScene):
	lNode = pScene.GetRootNode()
	if lNode:
		for i in range(lNode.GetChildCount()):
			lChildNode = lNode.GetChild(i)
			print("CHILD:", lChildNode.GetName())
			print("CHILD MESH:", lChildNode.GetMesh())

			if lChildNode.GetNodeAttribute() != None:
				lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())
				if lAttributeType == FbxNodeAttribute.eMesh:
					lMesh = lChildNode.GetNodeAttribute()
					lPoly = lMesh.GetPolygonCount()
					print("\nMESH NAME :: %s" % lMesh.GetName())
					print("MESH POLYGONS :: %i" % lPoly)
					print("MESH EDGES :: %i" % lMesh.GetMeshEdgeCount())
					polyVertices = lMesh.GetPolygonVertices()
					print(polyVertices)
					print("MESH VertexCount :: %i" % lMesh.GetPolygonVertexCount())
					print("MESH Layers :: %i" % lMesh.GetLayerCount())
					layer = lMesh.GetLayer(0)
					print(layer)
					print(layer.GetUVSetCount())
					print(layer.GetNormals())
					print(layer.GetTangents()) #NONE
					print(layer.GetBinormals()) #NONE
					print(layer.GetPolygonGroups()) #NONE
					print(layer.GetVertexColors()) #NONE
					print(layer.GetUVs()) # print(layer.GetLayerElementOfType(FbxLayerElement.eUV))
					print(layer.GetMaterials())
					print(layer.GetTextures(FbxLayerElement.eTextureDiffuse)) #NONE

					for materialIndex in range( 0, lChildNode.GetMaterialCount() ):
						material = lChildNode.GetMaterial( materialIndex )
						print(" material:", material, material.GetName())
						for propertyIndex in range( 0, FbxLayerElement.sTypeTextureCount() ):
							property = material.FindProperty( FbxLayerElement.sTextureChannelNames( propertyIndex ) )
							print("  property:", property, property.GetName())
							texture = property.GetSrcObject()
							print("   texture:", texture)
							if texture:
								textureFilename = texture.GetFileName()
								print("   ", texture.GetName())
								print("   filename:", textureFilename)

					uvSets = layer.GetUVSets()
					print("UV SETS:",uvSets)
					uvSet = uvSets[0]
					print("UV SET:", uvSet)

					uvDirect = uvSet.GetDirectArray() # array uv coords for
					uvIndexes = uvSet.GetIndexArray()

					uvElem = layer.GetUVs()
					uvElemD = uvElem.GetDirectArray()
					uvElemI = uvElem.GetIndexArray()

					controlPoints = lMesh.GetControlPoints()

					for p in range(lPoly):
						pSize = lMesh.GetPolygonSize(p)
						# pPoly = []
						# pUV = []
						for v in range(pSize):
							vertexIndex = lMesh.GetPolygonVertex(p, v)
							uvIndex = lMesh.GetTextureUVIndex(p, v)
							# pPoly.append(controlPoints[vertexIndex])
							# pUV.append(uvElemD.GetAt(uvIndex))
							point = controlPoints[vertexIndex]
							print("POINT:", point[0], point[1], point[2], point[3])

						# print("POLY:",pPoly, pUV)
					# for p in range(lPoly):
					# 	pSize = lMesh.GetPolygonSize(p)
					# 	pGroup = lMesh.GetPolygonGroup(p)
					# 	pStart = lMesh.GetPolygonVertexIndex(p)
					# 	print("   POLYGON {} | start: {} | size: {} | group: {}".format(p, pStart, pSize, pGroup))
					# 	for v in range(pSize):
					# 		vertexIndex = lMesh.GetPolygonVertex(p, v)
					# 		uvIndex = lMesh.GetTextureUVIndex(p, v)
					# 		print("   VERTEX {} :: {} ||| pos: {} || uv: {} index {} || uv: {} index {}".format(
					# 			v,
					# 			vertexIndex,
					# 			controlPoints[vertexIndex],
					# 			uvDirect.GetAt(uvIndex),
					# 			uvIndexes.GetAt(uvIndex),
					# 			uvElemD.GetAt(uvIndex),
					# 			uvElemI.GetAt(uvIndex)
					# 			))
