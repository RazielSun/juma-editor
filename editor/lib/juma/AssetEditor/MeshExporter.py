

#!/usr/bin/env python

import os.path
import time
import logging

from PySide                   	import QtCore, QtGui, QtOpenGL
from PySide.QtCore            	import Qt

from fbx import *
import FbxCommon
import fbxsip

from juma.core                	import signals, app
from AssetEditor             	import AssetEditorModule

##----------------------------------------------------------------##
class MeshExporter( AssetEditorModule ):
	"""docstring for MeshExporter"""
	_name = 'mesh_exporter'
	_dependency = [ 'qt', 'moai', 'asset_editor' ]

	def __init__(self):
		super(MeshExporter, self).__init__()

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
		print("load Trigger")
		self.openFBXFile()

	def saveTrigger( self ):
		print("save Trigger")

	##----------------------------------------------------------------##
	def openFBXFile( self ):
		fileName, filt = self.getSceneEditor().openFile( "FBX (*.fbx)", "Open FBX File" )
		if fileName:
			# Prepare the FBX SDK.
			lSdkManager, lScene = FbxCommon.InitializeSdkObjects()

			# Open FBX file
			print("open fbx file:", fileName)
			lResult = FbxCommon.LoadScene(lSdkManager, lScene, fileName)

			ListAllMeshesCount( lScene )
			TraceAllMeshes( lScene )

			# newName = 'output.fbx'
			# path = os.path.dirname( fileName )
			# FbxCommon.SaveScene(lSdkManager, lScene, path + '/' + newName)

			# Destroy all objects created by the FBX SDK.
			lSdkManager.Destroy()

##----------------------------------------------------------------##
def ListAllMeshesCount(pScene):
	print("NUMBER OF GEOMETRIES :: %i" % pScene.GetGeometryCount())

def TraceAllMeshes(pScene):
	lNode = pScene.GetRootNode()
	if lNode:
		for i in range(lNode.GetChildCount()):
			lChildNode = lNode.GetChild(i)
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
					uvSets = layer.GetUVSets()
					print("UV SETS:",uvSets)
					uvSet = uvSets[0]
					print("UV SET:", uvSet)
					print(layer.GetUVSetCount())
					print(layer.GetPolygonGroups())
					print(layer.GetVertexColors())
					print(layer.GetUVs()) # print(layer.GetLayerElementOfType(FbxLayerElement.eUV))
					print(layer.GetMaterials())
					print(layer.GetTextures(FbxLayerElement.eTextureDiffuse))

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

##----------------------------------------------------------------##

MeshExporter().register()
