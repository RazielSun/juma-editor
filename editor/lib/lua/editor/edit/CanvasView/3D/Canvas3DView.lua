
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

	self.props = {}
	self.models = {}
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
function Canvas3DView:createProp()
	local prop = MOAIProp.new()
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK )
	-- prop:seekRot ( 180, 360, 0, 10 )
	self.layer:insertProp( prop )
	table.insert( self.props, prop )
	return prop
end

function Canvas3DView:clearProps()
	for _, prop in ipairs(self.props) do
		self.layer:removeProp( prop )
	end
	self.props = {}
end

function Canvas3DView:createPropFromModels()
	for i, model in ipairs(self.models) do
		local prop = self:createProp()
		prop:setDeck( model:getMesh() )
		prop:setLoc( unpack(model.loc) )
		prop:setRot( unpack(model.rot) )
	end
end

---------------------------------------------------------------------------------
function Canvas3DView:addModel( model )
	table.insert( self.models, model )
end

function Canvas3DView:clearModels()
	for i, m in ipairs(self.models) do
		self.models[i] = nil
	end
	self.models = {}
end

function Canvas3DView:createModel( node, params )
	print("createModel", node, params)
	local ftype = params.getFormat( params )
	if ftype == 'FBX' then
		self:renderFBX( node, params )
	elseif ftype == 'OBJ' then
		self:renderOBJ( node, params )
	end
end

---------------------------------------------------------------------------------
function Canvas3DView:renderNode( node, params )
	self:clearModels()
	self:createModel( node, params )

	self:clearProps()
	self:createPropFromModels()

	self:updateCanvas()
end

function Canvas3DView:renderFBX( rootNode, obj )
	local size = obj.getPerPixel( obj )

	self:createMeshFromFBX( rootNode, rootNode, size )
end

function Canvas3DView:createMeshFromFBX( node, rootNode, size )
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

function Canvas3DView:renderOBJ( node, obj )
	local size = obj.getPerPixel( obj )

	local model = OBJObject( size )
	model:setOBJMaterials( node )
	model:setNode( node )
	model:createMesh()

	self:addModel( model )
end

---------------------------------------------------------------------------------
function Canvas3DView:saveBy( path )
	for i, model in ipairs(self.models) do
		model:save( path )
	end
end

---------------------------------------------------------------------------------

return Canvas3DView
