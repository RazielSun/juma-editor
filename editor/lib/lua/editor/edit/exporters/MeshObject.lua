
---------------------------------------------------------------------------------
--
-- @type MeshObject
--
---------------------------------------------------------------------------------

local MeshObject = Class("MeshObject")

function MeshObject:init()
	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	-- vertexFormat:declareNormal( 2, MOAIVertexFormat.GL_FLOAT, 3 )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )
	self.vertexFormat = vertexFormat

	local vbo = MOAIVertexBuffer.new ()
	self.vbo = vbo

	-- local ibo = MOAIIndexBuffer.new ()
	-- ibo:setIndexSize ( 2 )
	-- ibo:reserve ( 36 * 2 )
	-- self.ibo = ibo

	self.nodeName = 'none'
	self.format = '.mesh'
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
function MeshObject:save( path )
	local data = MOAISerializer.serializeToString(self.mesh)
	-- path = path or ''
	local fullPath = 'assets/3ds/' .. self.nodeName ..self.format
	MOAIFileSystem.saveFile(fullPath, data)
end

---------------------------------------------------------------------------------

return MeshObject
