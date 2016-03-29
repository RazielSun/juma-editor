
local EditorEntity = require("edit.EditorEntity")
local CanvasGrid = require("edit.CanvasView.CanvasGrid")
local CanvasFrame = require("edit.CanvasView.CanvasFrame")
local CanvasNavigate = require("edit.CanvasView.CanvasNavigate")
local CanvasToolManager = require("edit.CanvasView.CanvasToolManager")
local CanvasItemManager = require("edit.CanvasView.CanvasItemManager")
local PickingManager = require("edit.CanvasView.PickingManager")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( EditorEntity, "CanvasView" )

function CanvasView:init( canvasEnv )
	self.canvasEnv = assert( canvasEnv )
	EditorEntity.init( self, params)
	self.layer = MOAILayer.new()
end

---------------------------------------------------------------------------------
function CanvasView:onLoad()
	self:initContext()
	self:initAddons()
end

function CanvasView:initContext()
	self:setName( '__scene_view__' )
	local inputDevice = createEditorCanvasInputDevice( self.canvasEnv )
	self.inputDevice = inputDevice
	-- inputDevice:addMouseListener( self.mouseEventHandler, self )
 --    inputDevice:addKeyListener( self.keyEventHandler, self )
end

function CanvasView:initAddons()
	self.grid = self:addChild( CanvasGrid() )
	-- self.frame = self:addChild( CanvasFrame() )
	self.nav = self:addChild( CanvasNavigate { inputDevice = self.inputDevice, camera = self.layer:getCamera() } )
	self.toolMgr = self:addChild( CanvasToolManager() )
	self.itemMgr = self:addChild( CanvasItemManager { inputDevice = self.inputDevice } )
	self.pickingManager = PickingManager()
	self.pickingManager:setTargetScene( self:getScene() )
end

---------------------------------------------------------------------------------
function CanvasView:resizeCanvas( w, h )
	local viewport = self.layer:getViewport()
	viewport:setSize(w,h)
	viewport:setScale(w,h)
	self.grid:resizeView( w, h )
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

function CanvasView:wndToWorld( x, y )
	return self.layer:wndToWorld( x, y )
	-- return self.cameraCom:wndToWorld( x, y )
end

function CanvasView:updateCanvas()
	self.canvasEnv.updateCanvas()
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