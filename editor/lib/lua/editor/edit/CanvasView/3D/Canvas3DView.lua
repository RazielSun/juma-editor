
local EditorEntity = require("edit.EditorEntity")
local Canvas3DDrawGrid = require("edit.CanvasView.3D.Canvas3DDrawGrid")
local Canvas3DLookAtObject = require("edit.CanvasView.3D.Canvas3DLookAtObject")

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

	local fb = self:getScene():getFrameBuffer()
	if fb then fb:setClearDepth( true ) end
end

function Canvas3DView:initContext()
	local inputDevice = createEditorCanvasInputDevice( self.canvasEnv )
	self.inputDevice = inputDevice
end

function Canvas3DView:initCamera()
	local camera = MOAICamera.new()
	local z = camera:getFocalLength ( 1000 )
	camera:setLoc ( 0, 0, z )
    self:getScene():setCameraForLayers( self:getScene():getRender(), camera )
    self.camera = camera
end

function Canvas3DView:initAddons()
	self.grid = self:add( Canvas3DDrawGrid() )
	self.nav = self:add( Canvas3DLookAtObject { camera = self.camera, inputDevice = self.inputDevice } )
end

---------------------------------------------------------------------------------
function Canvas3DView:resizeCanvas( w, h )
	local viewport = self.layer:getViewport()
	if viewport then
		viewport:setSize(w,h)
		viewport:setScale(w,h)
	end
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
end

function Canvas3DView:updateCanvas()
	self.canvasEnv.updateCanvas()
end

---------------------------------------------------------------------------------

return Canvas3DView
