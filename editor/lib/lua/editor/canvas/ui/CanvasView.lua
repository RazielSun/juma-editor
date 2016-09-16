
local CoreCanvas = require("canvas.CanvasView")
local CanvasNavigate = require("canvas.CanvasNavigate")
local CanvasGrid = require("canvas.CanvasGrid")
local CanvasFrame = require("canvas.ui.CanvasFrame")

local CanvasToolManager = require("canvas.managers.CanvasToolManager")
local CanvasItemManager = require("canvas.managers.CanvasItemManager")
local PickingManager = require("canvas.managers.PickingManager")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( CoreCanvas, "CanvasUIView" )

---------------------------------------------------------------------------------
function CanvasView:initViewport()
	local viewport = self:getScene().viewport
	self.layer:setViewport( viewport )
	self:getScene():getLayer():setViewport( viewport )
	self.viewport = viewport
end

function CanvasView:initCamera()
	CoreCanvas.initCamera(self)
	local screen = self:getScene():getRootGroup()
	screen.defaultLayer:setCamera( self.camera )
end

function CanvasView:initAddons()
	self.grid = self:add( CanvasGrid() )
	self.frame = self:add( CanvasFrame( { ui = self:getScene().jui } ) )
	self.nav = self:add( CanvasNavigate { inputDevice = self.inputDevice, camera = self.camera } )
	self.toolMgr = self:add( CanvasToolManager() )
	self.itemMgr = self:add( CanvasItemManager { inputDevice = self.inputDevice } )
	self.pickingManager = PickingManager { scene = self:getScene() }
end

---------------------------------------------------------------------------------
function CanvasView:resizeFrame( w, h )
	if self.frame then
		self.frame:resize( w, h )
		self:updateCanvas()
	end
end

---------------------------------------------------------------------------------

return CanvasView
