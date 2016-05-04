
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
function Canvas3DView:renderNode( node, params )
	self:clearProps()

	print("renderNode", node, params)
	local ftype = params.getFormat( params )
	if ftype == 'FBX' then
		self:renderFBX( node, params )
	elseif ftype == 'OBJ' then
		self:renderOBJ( node, params )
	end

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
				local model = FBXObject( child, size )
				model:setFBXMaterials( child, rootNode.FbxLayerElement )
				model:setNode( child )
				model:createMesh()

				local prop = self:createProp()
				prop:setDeck( model:getMesh() )
			end
		end
	end
end

function Canvas3DView:renderOBJ( node, obj )
	--OBJObject( node, pixels )
	--obj.getPerPixel()
end

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

---------------------------------------------------------------------------------

return Canvas3DView
