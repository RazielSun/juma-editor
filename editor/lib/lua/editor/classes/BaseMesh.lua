
---------------------------------------------------------------------------------
--
-- @type BaseMesh
--
---------------------------------------------------------------------------------

local BaseMesh = Class("BaseMesh")

function BaseMesh:init()
	self.loc = {0,0,0}
	self.rot = {0,0,0}
	self.scl = {1,1,1}
	
	self.nodeName = 'none'
	self.format = '.mesh'
end

function BaseMesh:initWithParams()
	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	-- vertexFormat:declareNormal( 2, MOAIVertexFormat.GL_FLOAT )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )
	self.vertexFormat = vertexFormat

	local vbo = MOAIVertexBuffer.new ()
	self.vbo = vbo

	-- local ibo = MOAIIndexBuffer.new ()
	-- self.ibo = ibo
end

---------------------------------------------------------------------------------
function BaseMesh:createMesh()
	local vbo = self.vbo
	local vertexFormat = self.vertexFormat

	local mesh = MOAIMesh.new ()
	mesh:setVertexBuffer( vbo, vertexFormat )
	mesh:setPrimType ( MOAIMesh.GL_TRIANGLES ) --GL_LINES )--
	mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) ) --LINE_SHADER_3D )) --
	mesh:setTotalElements( vbo:countElements( vertexFormat ) )
	mesh:setBounds( vbo:computeBounds( vertexFormat ) )

	local texturePath = self._texturePath
	if texturePath then
		mesh:setTexture ( ResourceMgr:getTexture(texturePath) )
	else
		mesh:setTexture ( editorAssetPath( 'grid.png') )
	end

	mesh.loc = self.loc
	mesh.rot = self.rot
	mesh.scl = self.scl

	self.mesh = mesh
end

function BaseMesh:getMesh()
	if not self.mesh then
		self:createMesh()
	end

	return self.mesh
end

---------------------------------------------------------------------------------
function BaseMesh:setTexture( textureName, texturePath )
	self._textureName = textureName
	self._texturePath = texturePath
	print("setTexture", textureName, texturePath)
end

function BaseMesh:setFace( points, idx, normals, uv )
	if idx then
		local total = #idx
		-- local str = 'setFace: ' .. total .. ' idx:'

		for i = 3, total do
			local id1, id2, id3 = i-1, i, 1
			self:setTriangle( idx[id1], idx[id2], idx[id3],
				points[idx[id1]], points[idx[id2]], points[idx[id3]],
				normals[id1], normals[id2], normals[id3],
				uv[id1], uv[id2], uv[id3])
		end
	end
end

function BaseMesh:setTriangle( id1, id2, id3, p1, p2, p3, n1, n2, n3, uv1, uv2, uv3 )
	self:setVertex( id1, p1, n1, uv1 )
	self:setVertex( id2, p2, n2, uv2 )
	self:setVertex( id3, p3, n3, uv3 )
end

function BaseMesh:setVertex( id, p, n, uv )
	--
end

---------------------------------------------------------------------------------
function BaseMesh:save( export_path )
	local data = MOAISerializer.serializeToString(self.mesh)
	local export_path = export_path or 'assets/3ds/'
	local fullPath = export_path .. self.nodeName ..self.format
	MOAIFileSystem.saveFile(fullPath, data)
end

---------------------------------------------------------------------------------

return BaseMesh
