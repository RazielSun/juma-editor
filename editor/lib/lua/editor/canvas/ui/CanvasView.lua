
local CoreCanvas = require("canvas.CanvasView")
local CanvasNavigate = require("canvas.CanvasNavigate")
local CanvasGrid = require("canvas.CanvasGrid")
local CanvasFrame = require("canvas.ui.CanvasFrame")

local CanvasToolManager = require("edit.CanvasView.CanvasToolManager")
local CanvasItemManager = require("edit.CanvasView.CanvasItemManager")
local PickingManager = require("edit.CanvasView.PickingManager")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( CoreCanvas, "CanvasUIView" )

---------------------------------------------------------------------------------
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
