
local EditorEntity = require("edit.EditorEntity")
local FBXObject = require("edit.exporters.FBXObject")
local OBJObject = require("edit.exporters.OBJObject")
local Canvas3DGrid = require("edit.CanvasView.3D.Canvas3DGrid")
local Canvas3DNavigate = require("edit.CanvasView.3D.Canvas3DNavigate")

---------------------------------------------------------------------------------
--
-- @type CanvasExporter3DView
--
---------------------------------------------------------------------------------

local CanvasExporter3DView = Class( EditorEntity, "CanvasExporter3DView" )

function CanvasExporter3DView:init( canvasEnv )
	self.canvasEnv = assert( canvasEnv )
	EditorEntity.init( self, { name = "CanvasExporter3DView" })

	self.layer = MOAILayer.new()

	self.props = {}
	self.models = {}
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:onLoad()
	self:initContext()
	self:initCamera()
	self:initAddons()

	local fb = self:getScene():getFrameBuffer()
	if fb then
		fb:setClearDepth( true )
	end
end

function CanvasExporter3DView:initContext()
	local inputDevice = createEditorCanvasInputDevice( self.canvasEnv )
	self.inputDevice = inputDevice
end

function CanvasExporter3DView:initCamera()
	local camera = MOAICamera.new()
	camera:setLoc ( 0, 0, camera:getFocalLength ( 1000 ))
    self:getScene():setCameraForLayers( self:getScene():getRender(), camera )
    self.camera = camera
end

function CanvasExporter3DView:initAddons()
	self.grid = self:add( Canvas3DGrid() )
	self.nav = self:add( Canvas3DNavigate { camera = self.camera, inputDevice = self.inputDevice } )
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:resizeCanvas( w, h )
	local viewport = self.layer:getViewport()
	if viewport then
		viewport:setSize(w,h)
		viewport:setScale(w,h)
	end

	-- self.grid:resizeView( w, h )
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:getScene()
	return self.scene
end

function CanvasExporter3DView:getInputDevice()
	return self.inputDevice
end

function CanvasExporter3DView:getCamera()
	return self.camera
end

function CanvasExporter3DView:wndToWorld( x, y )
	return self.layer:wndToWorld( x, y )
end

function CanvasExporter3DView:updateCanvas()
	self.canvasEnv.updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:createProp()
	local prop = MOAIProp.new()
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK ) --CULL_FRONT ) --
	prop:setDepthTest( MOAIGraphicsProp.DEPTH_TEST_LESS ) --DEPTH_TEST_LESS_EQUAL
	self.layer:insertProp( prop )
	table.insert( self.props, prop )
	return prop
end

function CanvasExporter3DView:clearProps()
	for _, prop in ipairs(self.props) do
		self.layer:removeProp( prop )
	end
	self.props = {}
end

function CanvasExporter3DView:createPropFromModels()
	for i, model in ipairs(self.models) do
		local prop = self:createProp()
		prop:setDeck( model:getMesh() )
		prop:setLoc( unpack(model.loc) )
		prop:setRot( unpack(model.rot) )
	end
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:addModel( model )
	table.insert( self.models, model )
end

function CanvasExporter3DView:clearModels()
	for i, m in ipairs(self.models) do
		self.models[i] = nil
	end
	self.models = {}
end

function CanvasExporter3DView:createModel( node, params )
	print("createModel", node, params)
	local ftype = params.getFormat( params )
	if ftype == 'FBX' then
		self:renderFBX( node, params )
	elseif ftype == 'OBJ' then
		self:renderOBJ( node, params )
	end
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:renderNode( node, params )
	self:clearModels()
	self:createModel( node, params )

	self:clearProps()
	self:createPropFromModels()

	self:updateCanvas()
end

function CanvasExporter3DView:renderFBX( rootNode, obj )
	local size = obj.getPerPixel( obj )

	self:createMeshFromFBX( rootNode, rootNode, size )
end

function CanvasExporter3DView:createMeshFromFBX( node, rootNode, size )
	local total = node.GetChildCount()

	for i = 0, total-1 do
		local child = node.GetChild(i)
		local totalChilds = child.GetChildCount()
		if totalChilds > 0 then
			self:createMeshFromFBX( child, rootNode, size )
		else
			local mesh = child.GetMesh()
			if mesh then
				local model = FBXObject( size )
				model:setFBXMaterials( child, rootNode.FbxLayerElement )
				model:setNode( child )
				model:createMesh()
				self:addModel( model )
			end
		end
	end
end

function CanvasExporter3DView:renderOBJ( node, obj )
	local size = obj.getPerPixel( obj )

	local model = OBJObject( size )
	model:setOBJMaterials( node )
	model:setNode( node )
	model:createMesh()

	self:addModel( model )
end

---------------------------------------------------------------------------------
function CanvasExporter3DView:saveBy( path )
	for i, model in ipairs(self.models) do
		model:save( path )
	end
end

---------------------------------------------------------------------------------

return CanvasExporter3DView
