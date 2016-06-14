
local CoreCanvas = require("canvas.CanvasView")

local CanvasDrawGrid = require("canvas.3d.CanvasDrawGrid")
local CanvasNavigate = require("canvas.3d.CanvasNavigate")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( CoreCanvas, "Canvas3DView" )

---------------------------------------------------------------------------------
function CanvasView:initCamera()
	local camera = MOAICamera.new()
	camera:setLoc( 0, 1000, 1000 )
	camera:setRot( -45, 0, 0 )
	self.layer:setCamera( camera )
	self:getScene():getLayer():setCamera( camera )
    self.camera = camera
end

function CanvasView:initAddons()
	self.drawGrid = self:add( CanvasDrawGrid { rotate = {90,0,0} } )
	self.nav = self:add( CanvasNavigate { camera = self.camera, inputDevice = self.inputDevice } )
end

function CanvasView:initOther()
	local fb = self:getScene():getFrameBuffer()
	if fb then
		fb:setClearDepth( true )
	end
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

return CanvasView
