
local MeshObject = require("edit.exporters.MeshObject")

---------------------------------------------------------------------------------
--
-- @type FBXObject
--
---------------------------------------------------------------------------------

local FBXObject = Class(MeshObject, "FBXObject")

function FBXObject:init( size )
	MeshObject.init( self )
	self._size = size or 256
end

---------------------------------------------------------------------------------
function FBXObject:setNode( node )
	self:initWithParams()

	self.nodeName = node.GetName()
	print("FBXObject setNode", node, self.nodeName)

 	local trsl = node.LclTranslation.Get()
 	self.loc = {trsl[0], trsl[1], trsl[2]}
 	local rot = node.LclRotation.Get()
 	self.rot = {rot[0],rot[1],rot[2]}
	local scl = node.LclScaling.Get()
	self.scl = {scl[0], scl[1], scl[2]}

	print("LOC", unpack(self.loc))
	print("ROT", unpack(self.rot))
	print("SCL", unpack(self.scl))

	local mesh = node.GetMesh()

	local polyCount = mesh.GetPolygonCount()
	local totalIndexes = 0

	for p = 0, polyCount-1 do
		local size = mesh.GetPolygonSize(p)

		local count = 3
		if size == 6 then count = 12
		elseif size == 5 then count = 9
		elseif size == 4 then count = 6
		end

		totalIndexes = totalIndexes + count
	end

	print("polyCount", polyCount, totalIndexes)
	self.vbo:reserve( totalIndexes * self.vertexFormat:getVertexSize() )

	self.ibo:setIndexSize ( 2 )
	self.ibo:reserve ( totalIndexes * 2 )

	local controlPoints = mesh.GetControlPoints()
	
	local layer = mesh.GetLayer( 0 )
	local uvs = layer.GetUVs()
	local uvArray = nil
	if uvs then
		uvArray = uvs.GetDirectArray()
	end

	local normals = layer.GetNormals()
	local normalsArray = nil
	if normals then
		normalsArray = normals.GetDirectArray()
	end

	for p = polyCount-1, 0, -1 do
		local polySize = mesh.GetPolygonSize(p)
		local poly = {}
		local uvp = {}
		local normalsp = {}
		-- print("POLY:", p)

		for v = 0, polySize-1 do
			local vertexIndex = mesh.GetPolygonVertex(p,v)
			table.insert(poly, vertexIndex)

			local normalPoint = normalsArray and normalsArray[vertexIndex]
			table.insert(normalsp, normalPoint)

			local uvIndex = mesh.GetTextureUVIndex(p,v)
			local uvPoint = uvArray and uvArray[uvIndex]
			table.insert(uvp, uvPoint)
			-- print("V:", vertexIndex, controlPoints[vertexIndex])
			-- print("NORMAL", normalsArray[uvIndex], normalsArray[vertexIndex])
		end
		-- print("total vertex:", #poly)

		self:setFace( controlPoints, poly, normalsp, uvp )
	end
end

function FBXObject:setVertex( id, p, n, uv )
	self.ibo:writeU16( id )
	local s = self._size
	local sx, sy, sz = unpack(self.scl)
	self.vbo:writeFloat ( p[0]*s*sx, p[1]*s*sy, p[2]*s*sz )
	-- self.vbo:writeFloat ( n[0], n[1], n[2] )
	self.vbo:writeFloat ( uv and uv[0] or 0, uv and 1.0-uv[1] or 0 )
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