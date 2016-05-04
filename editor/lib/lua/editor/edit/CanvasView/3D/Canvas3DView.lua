
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
		self:updateCanvas()
	end
end

---------------------------------------------------------------------------------

return Canvas3DView
