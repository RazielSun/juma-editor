
local MeshObject = require("edit.exporters.MeshObject")

---------------------------------------------------------------------------------
--
-- @type FBXObject
--
---------------------------------------------------------------------------------

local FBXObject = Class(MeshObject, "FBXObject")

function FBXObject:init( rootNode, size )
	MeshObject.init( self )
	self._size = size or 256
end

---------------------------------------------------------------------------------
function FBXObject:setNode( node )
	self:initWithParams()

	print("FBXObject setNode", node)
	self.nodeName = node.GetName()
	local mesh = node.GetMesh()

	local polyCount = mesh.GetPolygonCount()
	local vertexCount = mesh.GetPolygonVertexCount()
	print("polyCount", polyCount)
	print("vertexCount", vertexCount)

	local totalIndexes = polyCount * 6
	self.vbo:reserve( totalIndexes * self.vertexFormat:getVertexSize() ) --polyCount * vertexCount )

	self.ibo:setIndexSize ( 2 )
	self.ibo:reserve ( totalIndexes * 2 )

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

		self:setFace( controlPoints, poly, normalsp, uvp )
	end
end

function FBXObject:setFace( points, idx, normals, uv )
	if idx then
		local total = #idx
		if total >= 3 then
			self:setTriangle( idx[1], idx[2], idx[3],
				points[idx[1]], points[idx[2]], points[idx[3]],
				normals[1], normals[2], normals[3],
				uv[1], uv[2], uv[3])
		end
		if total == 4 then
			self:setTriangle( idx[3], idx[4], idx[1],
				points[idx[3]], points[idx[4]], points[idx[1]],
				normals[3], normals[4], normals[1],
				uv[3], uv[4], uv[1])
		end
	end
end

function FBXObject:setTriangle( id1, id2, id3, p1, p2, p3, n1, n2, n3, uv1, uv2, uv3 )
	-- print("setTriangle")
	self:setVertex( id1, p1, n1, uv1 )
	self:setVertex( id2, p2, n2, uv2 )
	self:setVertex( id3, p3, n3, uv3 )
end

function FBXObject:setVertex( id, p, n, uv )
	self.ibo:writeU16( id )

	local sz = self._size
	-- print("setVertex", p[0], p[1], p[2], "uv", uv[0], uv[1])
	self.vbo:writeFloat ( p[0]*sz, p[1]*sz, p[2]*sz )
	-- self.vbo:writeFloat ( n[0], n[1], n[2] )
	self.vbo:writeFloat ( uv[0], uv[1] )
	self.vbo:writeColor32 ( 1, 1, 1 )
end

---------------------------------------------------------------------------------
function FBXObject:setFBXMaterials( node, element )
	local totalMaterials = node.GetMaterialCount()
	local totalProperty = element.sTypeTextureCount()

	for i = 0, totalMaterials-1 do
		local material = node.GetMaterial( i )
		for p = 0, totalProperty-1 do
			local property = material.FindProperty( element.sTextureChannelNames( p ) )
			local texture = property.GetSrcObject()
			if texture then
				self:setTexture( texture.GetName(), texture.GetFileName() )
			end
		end
	end
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



	-- # def parseFBXScene( self, scene, fileName ):
	-- # 	runtime = self.getRuntime()
	-- # 	rootNode = scene.GetRootNode()
	-- # 	for i in range(rootNode.GetChildCount()):
	-- # 		child = rootNode.GetChild(i)
	-- # 		mesh = child.GetMesh()
	-- # 		if mesh:
	-- # 			meshLua = runtime.getNewMeshExporter()
	-- # 			meshLua.setNode( meshLua, child )
	-- # 			meshLua.createMOAIMesh( meshLua )
	-- # 			path = os.path.dirname(fileName)
	-- # 			meshLua.save( meshLua, path )
		


-- def TraceAllMeshes(pScene):
-- 	lNode = pScene.GetRootNode()
-- 	if lNode:
-- 		for i in range(lNode.GetChildCount()):
-- 			lChildNode = lNode.GetChild(i)
-- 			print("CHILD:", lChildNode.GetName())
-- 			print("CHILD MESH:", lChildNode.GetMesh())

-- 			if lChildNode.GetNodeAttribute() != None:
-- 				lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())
-- 				if lAttributeType == FbxNodeAttribute.eMesh:
-- 					lMesh = lChildNode.GetNodeAttribute()
-- 					lPoly = lMesh.GetPolygonCount()
-- 					print("\nMESH NAME :: %s" % lMesh.GetName())
-- 					print("MESH POLYGONS :: %i" % lPoly)
-- 					print("MESH EDGES :: %i" % lMesh.GetMeshEdgeCount())
-- 					polyVertices = lMesh.GetPolygonVertices()
-- 					print(polyVertices)
-- 					print("MESH VertexCount :: %i" % lMesh.GetPolygonVertexCount())
-- 					print("MESH Layers :: %i" % lMesh.GetLayerCount())
-- 					layer = lMesh.GetLayer(0)
-- 					print(layer)
-- 					print(layer.GetUVSetCount())
-- 					print(layer.GetNormals())
-- 					print(layer.GetTangents()) #NONE
-- 					print(layer.GetBinormals()) #NONE
-- 					print(layer.GetPolygonGroups()) #NONE
-- 					print(layer.GetVertexColors()) #NONE
-- 					print(layer.GetUVs()) # print(layer.GetLayerElementOfType(FbxLayerElement.eUV))
-- 					print(layer.GetMaterials())
-- 					print(layer.GetTextures(FbxLayerElement.eTextureDiffuse)) #NONE

-- 					for materialIndex in range( 0, lChildNode.GetMaterialCount() ):
-- 						material = lChildNode.GetMaterial( materialIndex )
-- 						print(" material:", material, material.GetName())
-- 						for propertyIndex in range( 0, FbxLayerElement.sTypeTextureCount() ):
-- 							property = material.FindProperty( FbxLayerElement.sTextureChannelNames( propertyIndex ) )
-- 							print("  property:", property, property.GetName())
-- 							texture = property.GetSrcObject()
-- 							print("   texture:", texture)
-- 							if texture:
-- 								textureFilename = texture.GetFileName()
-- 								print("   ", texture.GetName())
-- 								print("   filename:", textureFilename)

-- 					uvSets = layer.GetUVSets()
-- 					print("UV SETS:",uvSets)
-- 					uvSet = uvSets[0]
-- 					print("UV SET:", uvSet)

-- 					uvDirect = uvSet.GetDirectArray() # array uv coords for
-- 					uvIndexes = uvSet.GetIndexArray()

-- 					uvElem = layer.GetUVs()
-- 					uvElemD = uvElem.GetDirectArray()
-- 					uvElemI = uvElem.GetIndexArray()

-- 					controlPoints = lMesh.GetControlPoints()

-- 					for p in range(lPoly):
-- 						pSize = lMesh.GetPolygonSize(p)
-- 						# pPoly = []
-- 						# pUV = []
-- 						for v in range(pSize):
-- 							vertexIndex = lMesh.GetPolygonVertex(p, v)
-- 							uvIndex = lMesh.GetTextureUVIndex(p, v)
-- 							# pPoly.append(controlPoints[vertexIndex])
-- 							# pUV.append(uvElemD.GetAt(uvIndex))
-- 							point = controlPoints[vertexIndex]
-- 							print("POINT:", point[0], point[1], point[2], point[3])

-- 						# print("POLY:",pPoly, pUV)
-- 					# for p in range(lPoly):
-- 					# 	pSize = lMesh.GetPolygonSize(p)
-- 					# 	pGroup = lMesh.GetPolygonGroup(p)
-- 					# 	pStart = lMesh.GetPolygonVertexIndex(p)
-- 					# 	print("   POLYGON {} | start: {} | size: {} | group: {}".format(p, pStart, pSize, pGroup))
-- 					# 	for v in range(pSize):
-- 					# 		vertexIndex = lMesh.GetPolygonVertex(p, v)
-- 					# 		uvIndex = lMesh.GetTextureUVIndex(p, v)
-- 					# 		print("   VERTEX {} :: {} ||| pos: {} || uv: {} index {} || uv: {} index {}".format(
-- 					# 			v,
-- 					# 			vertexIndex,
-- 					# 			controlPoints[vertexIndex],
-- 					# 			uvDirect.GetAt(uvIndex),
-- 					# 			uvIndexes.GetAt(uvIndex),
-- 					# 			uvElemD.GetAt(uvIndex),
-- 					# 			uvElemI.GetAt(uvIndex)
-- 					# 			))