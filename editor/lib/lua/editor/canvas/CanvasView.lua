
local EditorEntity = require("core.EditorEntity")
local CanvasNavigate = require("canvas.CanvasNavigate")
local CanvasGrid = require("canvas.CanvasGrid")

local CanvasToolManager = require("canvas.managers.CanvasToolManager")
local CanvasItemManager = require("canvas.managers.CanvasItemManager")
local PickingManager = require("canvas.managers.PickingManager")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( EditorEntity, "CanvasView" )

function CanvasView:init( env )
	self.env = assert( env )
	EditorEntity.init( self, { name = "CanvasView" })
	self.layer = MOAILayer.new()
end

---------------------------------------------------------------------------------
function CanvasView:onLoad()
	self:initContext()
	self:initViewport()
	self:initCamera()
	self:initAddons()
	self:initOther()
end

function CanvasView:initContext()
	local inputDevice = createEditorCanvasInputDevice( self.env )
	self.inputDevice = inputDevice
end

function CanvasView:initViewport()
	local viewport = MOAIViewport.new()
	self.layer:setViewport( viewport )
	self:getScene():getLayer():setViewport( viewport )
	self.viewport = viewport
end

function CanvasView:initCamera()
	local camera = MOAICamera2D.new()
	self.layer:setCamera( camera )
	self:getScene():getLayer():setCamera( camera )
    self.camera = camera
end

function CanvasView:initAddons()
	self.grid = self:add( CanvasGrid() )
	self.nav = self:add( CanvasNavigate { inputDevice = self.inputDevice, camera = self.camera } )
	self.toolMgr = self:add( CanvasToolManager() )
	self.itemMgr = self:add( CanvasItemManager { inputDevice = self.inputDevice } )
	self.pickingManager = PickingManager { scene = self:getScene() }
end

function CanvasView:initOther()
end

---------------------------------------------------------------------------------
function CanvasView:resizeCanvas( w, h )
	local viewport = self.viewport
	if viewport then
		viewport:setSize(w,h)
		viewport:setScale(w,h)
	end

	if self.grid then
		self.grid:resizeView( w, h )
	end
end

---------------------------------------------------------------------------------
function CanvasView:changeVisibleGrid()
	local vis = not self.grid.visible
	self.grid:setVisible( vis )
	self.grid.visible = vis
	self:updateCanvas()
end

function CanvasView:cameraZoom( zoomType )
	if zoomType == 'normal' then
		self.nav:setZoom( 1 )
	elseif zoomType == 'in' then
		self.nav:setZoom( self.nav:getZoom() + 0.5 )
	elseif zoomType == 'out' then
		self.nav:setZoom( self.nav:getZoom()- 0.5 )
	end
end

function CanvasView:moveCameraToSelected()
	self.nav:moveCameraToSelected()
	self:updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasView:getScene()
	return self.scene
end

function CanvasView:getInputDevice()
	return self.inputDevice
end

function CanvasView:getCamera()
	return self.camera
end

function CanvasView:wndToWorld( x, y )
	return self.layer:wndToWorld( x, y )
end

function CanvasView:updateCanvas()
	self.env.updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasView:addCanvasItem( item )
	self.itemMgr:addItem( item )
end

function CanvasView:removeCanvasItem( item )
	self.itemMgr:removeItem( item )
end

function CanvasView:changeEditTool( name )
	self.toolMgr:setTool( name )
end

function CanvasView:onSelectionChanged( selection )
	self.toolMgr:onSelectionChanged( selection )
end

---------------------------------------------------------------------------------
function CanvasView:pick( x, y )
	return self.pickingManager:pickPoint( x, y, pad )
end

function CanvasView:pickRect( x0, y0, x1, y1, pad )
	return self.pickingManager:pickRect( x0, y0, x1, y1, pad )
end

function CanvasView:pickAndSelect( x, y, pad )
	local picked = self:pick( x, y, pad )
	changeSelection( 'scene', unpack( picked ) )
	return picked
end

---------------------------------------------------------------------------------

return CanvasView
