
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

	local totalIndexes = 0
	for f = 0, faceCount-1 do
		local faceSize = node.GetFaceSize(node, f)
		if faceSize == 4 then
			totalIndexes = totalIndexes + 6
		else
			totalIndexes = totalIndexes + 3
		end
	end
	self.vbo:reserve( totalIndexes * self.vertexFormat:getVertexSize() )

	-- self.ibo:setIndexSize ( 2 )
	-- self.ibo:reserve ( totalIndexes * 2 )

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

			uvv = controlUV[uvi-1]
			if uvv and uvv~= '' then
				table.insert(uvp, uvv)
			end

			table.insert(normalsp, normals[ni-1])
		end

		self:setFace( controlPoints, poly, normalsp, uvp )
	end
end

function OBJObject:setVertex( id, p, n, uv )
	-- self.ibo:writeU16( id )
	local sz = self._size
	self.vbo:writeFloat ( tonumber(p[0])*sz, tonumber(p[1])*sz, tonumber(p[2])*sz )
	-- self.vbo:writeFloat ( tonumber(n[0]), tonumber(n[1]), tonumber(n[2]) )
	self.vbo:writeFloat ( uv and tonumber(uv[0]) or 0, uv and 1.0-tonumber(uv[1]) or 0 )
	self.vbo:writeColor32 ( 1, 1, 1 )
end

function OBJObject:setOBJMaterials( node )
	local mat = node.GetMaterial( node )
	if mat then
		self:setTexture( mat.GetTextureName( mat ), mat.GetTexturePath( mat ) )
	end
end

---------------------------------------------------------------------------------

return OBJObject
