
---------------------------------------------------------------------------------
--
-- @type MeshObject
--
---------------------------------------------------------------------------------

local MeshObject = Class("MeshObject")

function MeshObject:init()
	self._textured = false

	self.nodeName = 'none'
	self.format = '.mesh'
end

function MeshObject:initWithParams()
	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	-- vertexFormat:declareNormal( 2, MOAIVertexFormat.GL_FLOAT, 3 )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )
	self.vertexFormat = vertexFormat

	local vbo = MOAIVertexBuffer.new ()
	self.vbo = vbo

	local ibo = MOAIIndexBuffer.new ()
	self.ibo = ibo
end

---------------------------------------------------------------------------------
function MeshObject:createMesh()
	local vbo = self.vbo
	local vertexFormat = self.vertexFormat

	local mesh = MOAIMesh.new ()
	mesh:setVertexBuffer( vbo, vertexFormat )
	local texturePath = self._texturePath
	if texturePath then
		mesh:setTexture ( texturePath )
	end
	mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )
	mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) )
	mesh:setTotalElements( vbo:countElements( vertexFormat ) )
	-- print("vbo:computeBounds( vertexFormat )", vbo:computeBounds( vertexFormat ), vbo, vertexFormat)
	mesh:setBounds( vbo:computeBounds( vertexFormat ) )

	self.mesh = mesh
end

function MeshObject:getMesh()
	if not self.mesh then
		self:createMesh()
	end

	return self.mesh
end

---------------------------------------------------------------------------------
function MeshObject:setTexture( textureName, texturePath )
	self._textureName = textureName
	self._texturePath = texturePath
	print("setTexture", textureName, texturePath)
end

function MeshObject:setFace( points, idx, normals, uv )
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

function MeshObject:setTriangle( id1, id2, id3, p1, p2, p3, n1, n2, n3, uv1, uv2, uv3 )
	self:setVertex( id1, p1, n1, uv1 )
	self:setVertex( id2, p2, n2, uv2 )
	self:setVertex( id3, p3, n3, uv3 )
end

function MeshObject:setVertex( id, p, n, uv )
	--
end

---------------------------------------------------------------------------------
function MeshObject:save( export_path )
	local data = MOAISerializer.serializeToString(self.mesh)
	-- path = path or ''
	local export_path = export_path or 'assets/3ds/'
	local fullPath = export_path .. self.nodeName ..self.format
	MOAIFileSystem.saveFile(fullPath, data)
end

---------------------------------------------------------------------------------

return MeshObject
