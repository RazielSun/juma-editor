#!/usr/bin/env python

import os.path
import time
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from juma.core                	import signals, app
from AssetEditor             	import AssetEditorModule

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
class MeshExporter( AssetEditorModule ):
	"""docstring for MeshExporter"""
	_name = 'mesh_exporter'
	_dependency = [ 'qt', 'moai', 'asset_editor' ]

	def __init__(self):
		super(MeshExporter, self).__init__()
		self.runtime = None

	def getRuntime(self):
		if not self.runtime:
			self.runtime = self.affirmModule('moai')
		return self.runtime

	def onLoad(self):
		self.window = self.requestDockWindow(
			'MeshExporter',
			title = 'Mesh Exporter',
			dock  = 'right',
			minSize = (300,200)
			)

		self.loadBtn = self.window.addWidget( QtGui.QToolButton() )
		self.saveBtn = self.window.addWidget( QtGui.QToolButton() )

		self.loadBtn.setText( "Load" )
		self.saveBtn.setText( "Save" )

		self.loadBtn.clicked.connect( self.loadTrigger )
		self.saveBtn.clicked.connect( self.saveTrigger )

	def loadTrigger( self ):
		if _gInstalledFBX:
			self.openFBXFile()

	def saveTrigger( self ):
		pass

	##----------------------------------------------------------------##
	def openFBXFile( self ):
		fileName, filt = self.getSceneEditor().openFile( "FBX (*.fbx)", "Open FBX File" )
		if fileName:
			# Prepare the FBX SDK.
			lSdkManager, lScene = FbxCommon.InitializeSdkObjects()

			# Open FBX file
			print("open fbx file:", fileName)
			lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)

			self.parseFBXScene( lScene )

			# ListAllMeshesCount( lScene )
			# TraceAllMeshes( lScene )

			# newName = 'output.fbx'
			# path = os.path.dirname( fileName )
			# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + newName)

			# Destroy all objects created by the FBX SDK.
			# lSdkManager.Destroy()

	def parseFBXScene( self, scene ):
		runtime = self.getRuntime()
		rootNode = scene.GetRootNode()
		for i in range(rootNode.GetChildCount()):
			child = rootNode.GetChild(i)
			mesh = child.GetMesh()
			if mesh:
				meshLua = runtime.getNewMeshExporter()
				meshLua.setNode( meshLua, child )
		

##----------------------------------------------------------------##

MeshExporter().register()

##----------------------------------------------------------------##
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
					print(lMesh.GetPolygonVertices())
					print("MESH VertexCount :: %i" % lMesh.GetPolygonVertexCount())
					print("MESH Layers :: %i" % lMesh.GetLayerCount())
					layer = lMesh.GetLayer(0)
					print(layer)
					print(layer.GetUVSetCount())

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
						pGroup = lMesh.GetPolygonGroup(p)
						pStart = lMesh.GetPolygonVertexIndex(p)
						print("   POLYGON {} | start: {} | size: {} | group: {}".format(p, pStart, pSize, pGroup))
						for v in range(pSize):
							vertexIndex = lMesh.GetPolygonVertex(p, v)
							uvIndex = lMesh.GetTextureUVIndex(p, v)
							print("   VERTEX {} :: {} ||| pos: {} || uv: {} index {} || uv: {} index {}".format(
								v,
								vertexIndex,
								controlPoints[vertexIndex],
								uvDirect.GetAt(uvIndex),
								uvIndexes.GetAt(uvIndex),
								uvElemD.GetAt(uvIndex),
								uvElemI.GetAt(uvIndex)
								))
