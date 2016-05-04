
local MeshObject = require("edit.exporters.MeshObject")

---------------------------------------------------------------------------------
--
-- @type FBXObject
--
---------------------------------------------------------------------------------

local FBXObject = Class(MeshObject, "FBXObject")

function FBXObject:init( node, size )
	MeshObject.init( self )

	self:setSize( size )
	self:setNode( node )
end

---------------------------------------------------------------------------------
function FBXObject:setNode( node )
	print("FBXObject setNode", node)
	self.nodeName = node.GetName()
	local mesh = node.GetMesh()

	local polyCount = mesh.GetPolygonCount()
	local vertexCount = mesh.GetPolygonVertexCount()
	print("polyCount", polyCount)
	print("vertexCount", vertexCount)
	self.vbo:reserve( polyCount * 6 * self.vertexFormat:getVertexSize() ) --polyCount * vertexCount )

	local controlPoints = mesh.GetControlPoints()
	local layer = mesh.GetLayer( 0 )
	local uvs = layer.GetUVs()
	local uvArray = uvs.GetDirectArray()

	local normals = layer.GetNormals()
	local normalsArray = normals.GetDirectArray()

	for p = 0, polyCount-1 do
		local polySize = mesh.GetPolygonSize(p)
		local poly = {}
		local uvp = {}
		local normalsp = {}
		print("POLY:", p)
		for v = 0, polySize-1 do
			local vertexIndex = mesh.GetPolygonVertex(p,v)
			table.insert(poly, vertexIndex)
			local uvIndex = mesh.GetTextureUVIndex(p,v)
			local uvPoint = uvArray[uvIndex]
			local normalPoint = normalsArray[vertexIndex]
			table.insert(uvp, uvPoint)
			table.insert(normalsp, normalPoint)

			print("V:", vertexIndex, controlPoints[vertexIndex])
			-- print("NORMAL", normalsArray[uvIndex], normalsArray[vertexIndex])
		end

		self:setPoly(
			controlPoints[poly[1]],
			controlPoints[poly[2]],
			controlPoints[poly[3]],
			controlPoints[poly[4]],
			normalsp[1], normalsp[2], normalsp[3], normalsp[4],
			uvp[1], uvp[2], uvp[3], uvp[4]
			)
	end
end

function FBXObject:setPoly( p1, p2, p3, p4, n1, n2, n3, n4, uv1, uv2, uv3, uv4 )
	self:setTriangle( p1, p2, p3, n1, n2, n3, uv1, uv2, uv3 )
	self:setTriangle( p3, p4, p1, n1, n3, n4, uv3, uv4, uv1 )
end

function FBXObject:setTriangle( p1, p2, p3, n1, n2, n3, uv1, uv2, uv3 )
	-- print("setTriangle")
	self:setVertex( p1, n1, uv1 )
	self:setVertex( p2, n2, uv2 )
	self:setVertex( p3, n3, uv3 )
end

function FBXObject:setVertex( p, n, uv )
	local sz = self._size
	-- print("setVertex", p[0], p[1], p[2], "uv", uv[0], uv[1])
	self.vbo:writeFloat ( p[0]*sz, p[1]*sz, p[2]*sz )
	-- print("setVertex",p[0]*sz, p[1]*sz, p[2]*sz)
	-- self.vbo:writeFloat ( n[0], n[1], n[2] )
	self.vbo:writeFloat ( uv[0], uv[1] )
	self.vbo:writeColor32 ( 1, 1, 1 )
end

function FBXObject:setTextureName( textureName, fileName )
	self.textureName = textureName
	self.fileName = fileName
end

---------------------------------------------------------------------------------

return FBXObject


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