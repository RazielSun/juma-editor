
local CoreCanvas = require("canvas.CanvasView")

local FBXObject = require("classes.FBXMesh")
local OBJObject = require("classes.OBJMesh")

local CanvasDrawGrid = require("canvas.3d.CanvasDrawGrid")
local CanvasLookAtObject = require("canvas.preview.CanvasLookAtObject")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( CoreCanvas, "CanvasPreviewView" )

---------------------------------------------------------------------------------
function CanvasView:initCamera()
	local camera = MOAICamera.new()
	camera:setLoc( 0, 0, 500 )
	self.layer:setCamera( camera )
	self:getScene():getLayer():setCamera( camera )
    self.camera = camera
end

function CanvasView:initAddons()
	self.drawGrid = self:add( CanvasDrawGrid { rotate = {90,0,0} } )
	self.nav = self:add( CanvasLookAtObject { camera = self.camera, inputDevice = self.inputDevice } )
end

function CanvasView:initOther()
	local fb = self:getScene():getFrameBuffer()
	if fb then
		fb:setClearDepth( true )
	end

	self.props = {}
	self.models = {}

	
	self.nav:setZoom( 1 )
end

---------------------------------------------------------------------------------
function CanvasView:addCanvasItem( item )
end

function CanvasView:removeCanvasItem( item )
end

function CanvasView:changeEditTool( name )
end

function CanvasView:onSelectionChanged( selection )
end

---------------------------------------------------------------------------------
function CanvasView:createProp()
	local prop = MOAIProp.new()
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK ) --CULL_FRONT ) --
	prop:setDepthTest( MOAIGraphicsProp.DEPTH_TEST_LESS ) --DEPTH_TEST_LESS_EQUAL
	self.layer:insertProp( prop )
	table.insert( self.props, prop )
	return prop
end

function CanvasView:clearProps()
	for _, prop in ipairs(self.props) do
		self.layer:removeProp( prop )
	end
	self.props = {}
end

function CanvasView:createPropFromModels()
	for i, model in ipairs(self.models) do
		local prop = self:createProp()
		prop:setDeck( model:getMesh() )
		prop:setLoc( unpack(model.loc) )
		prop:setRot( unpack(model.rot) )
		prop:setScl( unpack(model.scl))
	end
end

---------------------------------------------------------------------------------
function CanvasView:addModel( model )
	table.insert( self.models, model )
end

function CanvasView:clearModels()
	for i, m in ipairs(self.models) do
		self.models[i] = nil
	end
	self.models = {}
end

function CanvasView:createModel( node, params )
	print("createModel", node, params)
	local ftype = params.GetFormat( params )
	if ftype == 'FBX' then
		self:renderFBX( node, params )
	elseif ftype == 'OBJ' then
		self:renderOBJ( node, params )
	end
end

---------------------------------------------------------------------------------
function CanvasView:renderNode( node, params )
	self:clearModels()
	self:createModel( node, params )

	self:clearProps()
	self:createPropFromModels()

	self:updateCanvas()
end

function CanvasView:renderFBX( rootNode, obj )
	local size = obj.GetPerPixel( obj )
	local texture = obj.GetTexture( obj, true )

	self:createMeshFromFBX( rootNode, rootNode, size, texture )
end

function CanvasView:createMeshFromFBX( node, rootNode, size, texture )
	if not node then return end
	
	local total = node.GetChildCount()

	for i = 0, total-1 do
		local child = node.GetChild(i)
		local totalChilds = child.GetChildCount()
		if totalChilds > 0 then
			self:createMeshFromFBX( child, rootNode, size, texture )
		else
			local mesh = child.GetMesh()
			if mesh then
				local model = FBXObject( size, texture )
				model:setFBXMaterials( child, rootNode.FbxLayerElement )
				model:setNode( child )
				model:createMesh()
				self:addModel( model )
			end
		end
	end
end

function CanvasView:renderOBJ( node, obj )
	local size = obj.getPerPixel( obj )

	local model = OBJObject( size )
	model:setOBJMaterials( node )
	model:setNode( node )
	model:createMesh()

	self:addModel( model )
end

---------------------------------------------------------------------------------
function CanvasView:saveBy( path )
	for i, model in ipairs(self.models) do
		model:save( path )
	end
end

---------------------------------------------------------------------------------

return CanvasView
