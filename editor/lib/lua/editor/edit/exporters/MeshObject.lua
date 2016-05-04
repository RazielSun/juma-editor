
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
