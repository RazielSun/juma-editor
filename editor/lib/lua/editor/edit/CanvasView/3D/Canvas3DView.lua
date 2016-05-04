
local EditorEntity = require("edit.EditorEntity")
local FBXObject = require("edit.exporters.FBXObject")
local OBJObject = require("edit.exporters.OBJObject")
-- local CanvasGrid = require("edit.CanvasView.CanvasGrid")

---------------------------------------------------------------------------------
--
-- @type Canvas3DView
--
---------------------------------------------------------------------------------

local Canvas3DView = Class( EditorEntity, "Canvas3DView" )

function Canvas3DView:init( canvasEnv )
	self.canvasEnv = assert( canvasEnv )
	EditorEntity.init( self, { name = "Canvas3DView" })
	self.layer = MOAILayer.new()
end

---------------------------------------------------------------------------------
function Canvas3DView:onLoad()
	self:initContext()
	self:initCamera()
	self:initAddons()
end

function Canvas3DView:initContext()
	-- local inputDevice = createEditorCanvasInputDevice( self.canvasEnv )
	-- self.inputDevice = inputDevice
end

function Canvas3DView:initCamera()
	local camera = MOAICamera.new()
	camera:setLoc ( 0, 0, camera:getFocalLength ( 1000 ))
	camera:setLoc( -500, 500, 500 )
	camera:lookAt( 0, 0, 0 )
	camera:setOrtho( false )
    self:getScene():setCameraForLayers( self:getScene():getRender(), camera )
    self.camera = camera
end

function Canvas3DView:initAddons()
	-- self.grid = self:add( CanvasGrid() )

	local prop = MOAIProp.new()
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK )
	-- prop:seekRot ( 180, 360, 0, 10 )
	self.layer:insertProp( prop )
	self.prop = prop
end

---------------------------------------------------------------------------------
function Canvas3DView:resizeCanvas( w, h )
	local viewport = self.layer:getViewport()
	if viewport then
		viewport:setSize(w,h)
		viewport:setScale(w,h)
	end

	-- self.grid:resizeView( w, h )
end

---------------------------------------------------------------------------------
function Canvas3DView:getScene()
	return self.scene
end

function Canvas3DView:getInputDevice()
	return self.inputDevice
end

function Canvas3DView:getCamera()
	return self.camera
end

function Canvas3DView:wndToWorld( x, y )
	return self.layer:wndToWorld( x, y )
	-- return self.cameraCom:wndToWorld( x, y )
end

function Canvas3DView:updateCanvas()
	self.canvasEnv.updateCanvas()
end

---------------------------------------------------------------------------------
function Canvas3DView:renderNode( node, nodeType, pixels )
	local meshparser = nil
	if nodeType == 'fbx' then
		meshparser = FBXObject( node, pixels )
	elseif nodeType == 'obj' then
		meshparser = OBJObject( node, pixels )
	end

	if meshparser then
		local mesh = meshparser:getMesh()
		self.prop:setDeck( mesh )
	end
end

function Canvas3DView:setMesh( mesh )
	local prop = MOAIProp.new()
	prop:setDeck( mesh )	
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK )
	-- prop:seekRot ( 180, 360, 0, 10 )
	self.layer:insertProp( prop )

	self.prop = prop
end

function Canvas3DView:createMesh()
	local vertexFormat = MOAIVertexFormat.new()
	vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3 )
	vertexFormat:declareUV( 2, MOAIVertexFormat.GL_FLOAT, 2 )
	vertexFormat:declareColor( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )

	local vbo = MOAIVertexBuffer.new ()
	vbo:reserve ( 36 * vertexFormat:getVertexSize ())

	local size = 256
	local vertexes = {}

	local addControlPoint = function( x, y, z )
		table.insert( vertexes, { x*size, y*size, z*size } )
	end

	addControlPoint( 0.5, 0.5, 0.5 ) -- 0 +
	addControlPoint( 0.5, 0.5, -0.5 ) -- 1 +
	addControlPoint( 0.5, -0.5, 0.5 ) -- 2 +
	addControlPoint( 0.5, -0.5, -0.5 ) -- 3 +
	addControlPoint( -0.5, 0.5, -0.5 ) -- 4 +
	addControlPoint( -0.5, 0.5, 0.5 ) -- 5 +
	addControlPoint( -0.5, -0.5, -0.5 ) -- 6 +
	addControlPoint( -0.5, -0.5, 0.5 ) -- 7 +

	local normals = {}
	local addNormal = function( x, y, z )
		table.insert(normals, {x,y,z})
	end

	addNormal( 1, 0, 0 )
	addNormal( 0, 1, 0 )
	addNormal( -1, 0, 0 )
	addNormal( 0, -1, 0 )
	addNormal( 0, 0, -1 )
	addNormal( 0, 0, 1 )

	local uvs = {}
	local addUVs = function( u, v )
		table.insert( uvs, {u,v} )
	end

	addUVs(0,0)
	addUVs(0,1)
	addUVs(1,1)
	addUVs(1,0)

	local color = {1,1,1}

	local setVertex = function( p, uv, n )
		vbo:writeFloat ( unpack(vertexes[p+1]) ) 
		vbo:writeFloat( unpack(uvs[uv]) )
		vbo:writeColor32 ( unpack(color) )
	end

	local setTriangle = function( p1, p2, p3, uv1, uv2, uv3, n )
		setVertex( p1, uv1, n )
		setVertex( p2, uv2, n )
		setVertex( p3, uv3, n )
	end

	local setPoly = function( p1, p2, p3, p4, uv1, uv2, uv3, uv4, n )
		setTriangle( p1, p2, p3, uv1, uv2, uv3, n )
		setTriangle( p3, p4, p1, uv3, uv4, uv1, n )
	end

	setPoly( 0, 2, 3, 1, 1, 2, 3, 4, 1 ) 
	setPoly( 4, 6, 7, 5, 1, 2, 3, 4, 1 )
	setPoly( 4, 5, 0, 1, 1, 2, 3, 4, 1 )
	setPoly( 7, 6, 3, 2, 1, 2, 3, 4, 1 )
	setPoly( 5, 7, 2, 0, 1, 2, 3, 4, 1 )
	setPoly( 1, 3, 6, 4, 1, 2, 3, 4, 1 )
	
	-- MESH
	local mesh = MOAIMesh.new ()

	mesh:setVertexBuffer( vbo, vertexFormat )
	mesh:setTexture ( editorAssetPath("moai.png") )
	mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )
	mesh:setShader ( MOAIShaderMgr.getShader( MOAIShaderMgr.MESH_SHADER ) )
	mesh:setTotalElements( vbo:countElements( vertexFormat ) )
	mesh:setBounds( vbo:computeBounds( vertexFormat ) )

	return mesh
end


---------------------------------------------------------------------------------

return Canvas3DView
