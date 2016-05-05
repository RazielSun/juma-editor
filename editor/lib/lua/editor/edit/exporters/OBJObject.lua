
local MeshObject = require("edit.exporters.MeshObject")

---------------------------------------------------------------------------------
--
-- @type OBJObject
--
---------------------------------------------------------------------------------

local OBJObject = Class(MeshObject, "OBJObject")

function OBJObject:init( size )
	MeshObject.init( self )
	self._size = size or 256
end

---------------------------------------------------------------------------------
function OBJObject:setNode( node )
	self:initWithParams()
	
	self.nodeName = node.GetName( node )
	print("OBJObject setNode", node, self.nodeName)

	local faceCount = node.GetFaceCount( node )
	print("faceCount", faceCount)

	local totalIndexes = faceCount * 6
	self.vbo:reserve( totalIndexes * self.vertexFormat:getVertexSize() )
	self.ibo:setIndexSize ( 2 )
	self.ibo:reserve ( totalIndexes * 2 )

	local controlPoints = node.GetVertexes( node )
	local controlUV = node.GetUV( node )
	local normals = node.GetNormals( node )

	-- print(controlPoints)
	-- print(controlUV)

	for f = 0, faceCount-1 do
		local faceSize = node.GetFaceSize(node, f)
		local poly = {}
		local uvp = {}
		local normalsp = {}
		-- print("FACE:", f)

		for v = 0, faceSize-1 do
			local data = node.GetFaceVertex(node, f,v)
			local vi, uvi, ni = tonumber(data[0]), tonumber(data[1]), tonumber(data[2])
			-- print("V:", vi, uvi, ni)
			table.insert(poly, vi-1)
			table.insert(uvp, controlUV[uvi-1])
			table.insert(normalsp, ni-1)
		end

		self:setFace( controlPoints, poly, normalsp, uvp )
	end
end

function OBJObject:setVertex( id, p, n, uv )
	self.ibo:writeU16( id )
	local sz = self._size
	self.vbo:writeFloat ( tonumber(p[0])*sz, tonumber(p[1])*sz, tonumber(p[2])*sz )
	-- self.vbo:writeFloat ( n[0], n[1], n[2] )
	self.vbo:writeFloat ( tonumber(uv[0]), tonumber(uv[1]) )
	self.vbo:writeColor32 ( 1, 1, 1 )
end

function OBJObject:setOBJMaterials( node )
	local mat = node.GetMaterial( node )
	self:setTexture( mat.GetTextureName( mat ), mat.GetTexturePath( mat ) )
end

---------------------------------------------------------------------------------

return OBJObject
