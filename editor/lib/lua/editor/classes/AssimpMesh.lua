
local BaseMesh = require("classes.BaseMesh")

---------------------------------------------------------------------------------
--
-- @type AssimpMesh
--
---------------------------------------------------------------------------------

local AssimpMesh = Class(BaseMesh, "AssimpMesh")

function AssimpMesh:init( size, texture )
	BaseMesh.init( self )
	self._size = size or 256
	self._texture = texture or ''
	self._bones = {}
end

---------------------------------------------------------------------------------
function AssimpMesh:setNode( node )
	local sz = self._size

	self.name = node.name

	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )
	self.vertexFormat = vertexFormat

	local vbo = MOAIVertexBuffer.new ()
	self.vbo = vbo

	local ibo = MOAIIndexBuffer.new ()
	self.ibo = ibo

	local vtxCount = node.verticesCount
    local idxCount = 3 * node.facesCount
    self.idxCount = idxCount

    ibo:setIndexSize ( 4 )
    ibo:reserve ( idxCount * 4 )

    vbo:reserve ( vtxCount * vertexFormat:getVertexSize ())

    for i = 0, vtxCount - 1 do
        local vtx = node.vertices [ i ]
        local uv = node.texturecoords [ 0 ][ i ]
        vbo:writeFloat ( sz * vtx [ 0 ], sz * vtx [ 1 ], sz * vtx [ 2 ])
        vbo:writeFloat ( uv [ 0 ], uv [ 1 ])
        vbo:writeColor32 ( 1, 1, 1, 1 )
    end

    for face in python.iter ( node.faces ) do
        ibo:writeU32 ( face [ 0 ], face [ 1 ], face [ 2 ])
    end

    local bones = {}
    for bname in python.iter ( node.bonesNames ) do
    	table.insert(bones, bname)
    end
    self._bones = bones
end

---------------------------------------------------------------------------------
function AssimpMesh:createMesh()
	local vbo = self.vbo
	local ibo = self.ibo
	local vertexFormat = self.vertexFormat

	local mesh = MOAIMesh.new ()

	mesh:setVertexBuffer( vbo, vertexFormat )
	mesh:setIndexBuffer ( ibo )
	
	mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )
	mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) )

	mesh:setTotalElements ( self.idxCount )
	mesh:setBounds( vbo:computeBounds( vertexFormat ) )

	local textureName = self._texture

	if not textureName or textureName == '' then
		local textureName = self._texturePath
		if not textureName then
			textureName = editorAssetPath( 'grid.png')
		end
	end

	if textureName then
		local texture = ResourceMgr:getTexture( textureName )
		mesh:setTexture ( texture )
	end

	mesh.bones = self._bones

	self.mesh = mesh
end

---------------------------------------------------------------------------------

return AssimpMesh
