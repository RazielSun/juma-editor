
local BaseMesh = require("classes.BaseMesh")

---------------------------------------------------------------------------------
--
-- @type AssimpMesh
--
---------------------------------------------------------------------------------

local AssimpMesh = Class(BaseMesh, "AssimpMesh")

function AssimpMesh:init()
	BaseMesh.init( self )
	self._bones = {}
end

---------------------------------------------------------------------------------
function AssimpMesh:setLightNode( node )
	local useBakeLight = node.GetBakeLight( node )
	local diffusePower = node.GetDiffusePower( node )
	local ambientLight = node.GetAmbientLight( node )
	local lightDirection = node.GetLightDirection( node )
	local useLightMap = node.GetUseLightMap( node )

	self.useBakeLight = useBakeLight
	self.diffusePower = diffusePower
	self.ambientLight = { ambientLight[0], ambientLight[1], ambientLight[2], ambientLight[3] }
	self.lightDirection = { lightDirection[0], lightDirection[1], lightDirection[2] }
	self.useLightMap = useLightMap
end

function AssimpMesh:luminosity(r, g, b)
	local light = self.ambientLight
	return light[1] * r + light[2] * g + light[3] * b
end

---------------------------------------------------------------------------------
function AssimpMesh:setNode( node )
	self.name = node.name
	print()
	print("AssimpMesh setNode", self.name)
	print()

	if self.useLightMap and node.uvcounts == 1 then
		self.useLightMap = false
	end

	self:initWithParams()

	local vertexFormat = self.vertexFormat
	local vbo = self.vbo
	local ibo = self.ibo

	local vtxCount = node.verticesCount
    local idxCount = 3 * node.facesCount

    local iboSize = 2 -- 2/4
    ibo:setIndexSize ( iboSize )
    ibo:reserve ( idxCount * iboSize )
    vbo:reserve ( vtxCount * vertexFormat:getVertexSize ())

    local sz = self._size

    for i = 0, vtxCount - 1 do
        local vtx = node.vertices [ i ]
        vbo:writeFloat ( sz * vtx [ 0 ], sz * vtx [ 1 ], sz * vtx [ 2 ] )

        local uv = node.texturecoords [ 0 ][ i ]
        vbo:writeFloat ( uv [ 0 ], uv [ 1 ] )
        
        if self.useLightMap then
        	local uv2 = node.texturecoords [ 1 ][ i ]
	        vbo:writeFloat ( uv2 [ 0 ], uv2 [ 1 ] )
        end

        if self.useBakeLight then
        	local n = node.normals [ i ]
        	local ambient = self.ambientLight
        	local diffuse = self.diffusePower
        	local luma = math.max(0, self:luminosity ( n [ 0 ], n [ 1 ], n [ 2 ]))
        	local r = math.min ( 1, ambient [ 1 ] + diffuse * luma )
            local g = math.min ( 1, ambient [ 2 ] + diffuse * luma )
            local b = math.min ( 1, ambient [ 3 ] + diffuse * luma )
            vbo:writeColor32 ( r, g, b, 1 )
        else
        	vbo:writeColor32 ( 1, 1, 1, 1 )
        end
    end

    for face in python.iter ( node.faces ) do
    	local sz = sizeOfPythonObject(face)
    	if sz >= 3 then
    		if iboSize == 4 then
		        ibo:writeU32 ( face [ 0 ], face [ 1 ], face [ 2 ] )
	        else
		       	ibo:writeU16 ( face [ 0 ], face [ 1 ], face [ 2 ] )
	        end
	        -- print("ibo:", face [ 0 ], face [ 1 ], face [ 2 ])
	    else
	    	print("AssimpMesh: FACE is BROKEN!")
	    end
    end

    -- ibo:printIndices()

    local bones = {}
    for bname in python.iter ( node.bonesNames ) do
    	table.insert(bones, bname)
    end

    self._bones = bones
    self._materialID = node.materialID

    self._vertexCount = vtxCount
    self._indexCount = idxCount
end

---------------------------------------------------------------------------------
function AssimpMesh:createMesh ( option )
	local option = option or {}
	local vbo = self.vbo
	local ibo = self.ibo
	local vertexFormat = self.vertexFormat

	local mesh = MOAIMesh.new ()

	mesh:setVertexBuffer( vbo, vertexFormat )
	mesh:setIndexBuffer ( ibo )
	
	mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )
	mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) )

	mesh:setTotalElements ( self._indexCount )
	mesh:setBounds( vbo:computeBounds( vertexFormat ) )

	mesh._vertexCount = self._vertexCount
	mesh._indexCount = self._indexCount

	if option.exportBuffers then
		mesh._vbo = vbo
		mesh._ibo = ibo
	end

	mesh._bones = self._bones
	mesh.material = self._material
	mesh.useLightMap = self.useLightMap

	local textureName = self:getTexture()
	if textureName then
		local texture = ResourceMgr:getTexture( textureName )
		mesh:setTexture ( texture )
	end

	self.canSave = option.exportMesh
	self.mesh = mesh
end

---------------------------------------------------------------------------------

return AssimpMesh
