
local MeshExporter = require("edit.exporters.MeshExporter")

---------------------------------------------------------------------------------
--
-- @type FBXExporter
--
---------------------------------------------------------------------------------

local FBXExporter = Class(MeshExporter, "FBXExporter")

function FBXExporter:init()
	MeshExporter.init( self )
end

---------------------------------------------------------------------------------
function FBXExporter:setNode( node )
	print("FBXExporter setNode", node)
end

---------------------------------------------------------------------------------

return FBXExporter


-- # lNode = pScene.GetRootNode()
-- # if lNode:
-- # 		for i in range(lNode.GetChildCount()):
-- # 			lChildNode = lNode.GetChild(i)
-- # print("CHILD:", lChildNode.GetName())
-- # 			print("CHILD MESH:", lChildNode.GetMesh())
-- # lPoly = lMesh.GetPolygonCount()
-- # print("MESH POLYGONS :: %i" % lPoly)
-- # print("MESH VertexCount :: %i" % lMesh.GetPolygonVertexCount())
-- # print("MESH Layers :: %i" % lMesh.GetLayerCount())
-- 					# layer = lMesh.GetLayer(0)
-- 					# uvElem = layer.GetUVs()
-- 					# uvElemD = uvElem.GetDirectArray()
-- 					# uvElemI = uvElem.GetIndexArray()

-- 					# controlPoints = lMesh.GetControlPoints()
-- 					# for p in range(lPoly):
-- 					# 	pSize = lMesh.GetPolygonSize(p)
-- 					# 	for v in range(pSize):
-- 					# 		vertexIndex = lMesh.GetPolygonVertex(p, v)
-- 					# 		uvIndex = lMesh.GetTextureUVIndex(p, v)
-- 					# 		print("   VERTEX {} ||| pos: {} || uv: {} index {}".format(
-- 					# 			vertexIndex, 0 
-- 					# 			controlPoints[vertexIndex], fbx.FbxVector4(0.500000, 0.500000, 0.500000, 0.000000)
-- 					# 			uvElemD.GetAt(uvIndex), fbx.FbxVector2(0.000000, 1.000000)
-- 					# 			uvElemI.GetAt(uvIndex), 0
-- 					# 			))
-- 					# for materialIndex in range( 0, lChildNode.GetMaterialCount() ):
-- 					# 	material = lChildNode.GetMaterial( materialIndex )
-- 					# 	print(" material:", material, material.GetName())
-- 					# 	for propertyIndex in range( 0, FbxLayerElement.sTypeTextureCount() ):
-- 					# 		property = material.FindProperty( FbxLayerElement.sTextureChannelNames( propertyIndex ) )
-- 					# 		print("  property:", property, property.GetName())
-- 					# 		texture = property.GetSrcObject()
-- 					# 		print("   texture:", texture)
-- 					# 		if texture:
-- 					# 			textureFilename = texture.GetFileName()
-- 					# 			print("   ", texture.GetName())
-- 					# 			print("   filename:", textureFilename)