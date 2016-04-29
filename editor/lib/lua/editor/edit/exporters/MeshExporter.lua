
---------------------------------------------------------------------------------
--
-- @type MeshExporter
--
---------------------------------------------------------------------------------

local MeshExporter = Class("MeshExporter")

function MeshExporter:init()
	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )
	self.vertexFormat = vertexFormat

	local vbo = MOAIVertexBuffer.new ()
	self.vbo = vbo
	--vbo:reserve ( 6 * vertexFormat:getVertexSize ()) -- 6 * 24
end

	-- # local sz = 128

	-- # local p1 = { pos={-sz,sz,0}, uv = {0,0}, color={1,1,1} }
	-- # local p2 = { pos={sz,sz,0}, uv = {1,0}, color={1,1,1} }
	-- # local p3 = { pos={sz,-sz,0}, uv = {1,1}, color={1,1,1} }
	-- # local p4 = { pos={-sz,-sz,0}, uv = {0,1}, color={1,1,1} }

---------------------------------------------------------------------------------
function MeshExporter:setPoly( p1, p2, p3, p4, uv1, uv2, uv3, uv4 )
	-- # setTriangle(p1, p2, p3)
	-- # setTriangle(p1, p3, p4)
end

function MeshExporter:setTriangle( p1, p2, p3, uv1, uv2, uv3 )
	-- # local setTriangle = function(t1,t2,t3)
	-- # 	setVertex(t1)
	-- # 	setVertex(t2)
	-- # 	setVertex(t3)
	-- # end
end

---------------------------------------------------------------------------------
function MeshExporter:setVertex( p, uv )
	self:setCoord( x, y, z )
	self:setUV( u, v )
	self:setColor( r, g, b )
	-- # local setVertex = function(p)
	-- # 	vbo:writeFloat ( unpack(p.pos) )
	-- # 	vbo:writeFloat ( unpack(p.uv) )
	-- # 	vbo:writeColor32 ( unpack(p.color) )
	-- # end
end

function MeshExporter:setCoord( x, y, z )
	--
end

function MeshExporter:setUV( u, v )
	--
end

function MeshExporter:setColor( r, g, b )
	--
end

function MeshExporter:setTexture( texture )
	--
end

---------------------------------------------------------------------------------
function MeshExporter:createMesh()
	-- # -- MESH
	-- # local mesh = MOAIMesh.new ()
	-- # mesh:setVertexBuffer( vbo, vertexFormat )
	-- # mesh:setTexture ( "moai.png" )
	-- # mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )
	-- # mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) )
	-- # mesh:setTotalElements( vbo:countElements( vertexFormat ) )
	-- # mesh:setBounds( vbo:computeBounds( vertexFormat ) )
end

---------------------------------------------------------------------------------
function MeshExporter:saveMesh()
 -- # -- moaiserializer.serializeToString(mesh)
end

---------------------------------------------------------------------------------

return MeshExporter
