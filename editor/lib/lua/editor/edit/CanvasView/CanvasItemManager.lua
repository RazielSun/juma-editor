
local EditorComponent = require("edit.EditorComponent")
local InputEvent = require("input.InputEvent")

---------------------------------------------------------------------------------
--
-- @type CanvasItemManager
--
---------------------------------------------------------------------------------

local CanvasItemManager = Class( EditorComponent, "CanvasItemManager" )

function CanvasItemManager:init( option )
	option = option or {}
	self.items = {}
	self.activeItem = nil
	self.activeMouseButton = nil

	self.factorZoom = 1

	self.ui = option.ui
	self.inputDevice = option.inputDevice

	EditorComponent.init(self, { name = "CanvasItemManager" })
end

function CanvasItemManager:onLoad()
	self.layer = self.ui and self.ui:getScreen(1).defaultLayer or self.entity.layer
	assert( self.layer )

	self.inputDevice:addListener( self )

	local cameraListenerNode = MOAIScriptNode.new()
	cameraListenerNode:setCallback( function() self:updateScaleAllItems() end )
	cameraListenerNode:setNodeLink( self:getNav().zoomControlNode ) --WTF? not updated
	self.cameraListenerNode = cameraListenerNode

	self:updateFactorZoom()
end

function CanvasItemManager:updateFactorZoom()
	self.factorZoom = 1 / self:getNav():getZoom()
end

function CanvasItemManager:getView()
	return self.entity
end

function CanvasItemManager:getNav()
	return self:getView().nav
end

---------------------------------------------------------------------------------
function CanvasItemManager:addItem( item )
	table.insert( self.items, 1, item )
	item.entity = self
	item:_load() -- item add to layer
	self:updateScaleForItem( item )
end

function CanvasItemManager:removeItem( item )
	if table.removeElement( self.items, item ) then
		item:setLayer( nil )
		item.entity = nil
	end
end

function CanvasItemManager:findTopItem( x, y, pad )
	for i, item in ipairs( self.items ) do
		if item:inside( x, y, 0, pad ) then
			return item
		end
	end
	return false
end

---------------------------------------------------------------------------------
function CanvasItemManager:updateScaleForItem( item )
	if item:isConstantSize() then
		local scl = self.factorZoom
		item:setScl( scl, scl, scl )
	end
end

function CanvasItemManager:updateScaleAllItems()
	self:updateFactorZoom()
	print("updateScaleAllItems", self.factorZoom)
	for i, item in ipairs( self.items ) do
		self:updateScaleForItem( item )
	end		
	self:getView():updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasItemManager:onInputEvent( event )
	if event.id == InputEvent.MOUSE_EVENT then
		self:onMouseEvent( event )
	elseif event.id == InputEvent.KEY_EVENT then
		self:onKeyEvent( event )
	end
end

function CanvasItemManager:onMouseEvent( event )
	if event.eventName == InputEvent.DOWN then
		self:onMouseDown( event.idx, event.wx, event.wy )
	elseif event.eventName == InputEvent.UP then
		self:onMouseUp( event.idx, event.wx, event.wy )
	elseif event.eventName == InputEvent.MOVE then
		self:onMouseMove( event.wx, event.wy )
	end
end

function CanvasItemManager:onMouseDown( btn, wx, wy )
	if self.activeItem then return end
	local item = self:findTopItem( wx, wy )
	if item then
		self.activeItem = item
		self.activeItem:onMouseDown( btn, wx, wy )
		self.activeMouseButton = btn	
	end
	-- self:focus( item )
end

function CanvasItemManager:onMouseUp( btn, wx, wy )
	if self.activeMouseButton == btn then
		self.activeItem:onMouseUp( btn, wx, wy )
		self.activeMouseButton = false
		self.activeItem = false
	end
end

function CanvasItemManager:onMouseMove( wx, wy )
	if self.activeMouseButton then
		self.activeItem:onMouseMove( wx, wy )
		return
	end

	-- local item = self:findTopItem( x, y )
	-- if item ~= self.hoverItem then
	-- 	if self.hoverItem then
	-- 		self.hoverItem:onMouseEnter()
	-- 	end
	-- 	self.hoverItem = item
	-- 	if item then
	-- 		item:onMouseLeave()
	-- 	end
	-- end

	-- if self.hoverItem then
	-- 	self.hoverItem:onMouseMove( x, y )
	-- end
end

function CanvasItemManager:onKeyEvent( event )
	local k = event.key
	if k=="down" or k=="up" or k=="left" or k=="right" then
		local topItem = self.items[1]
		if topItem and topItem.onArrowsPressed then
			topItem:onArrowsPressed( k, event.down, self.inputDevice:isShiftDown() )
		end
	end
end


---------------------------------------------------------------------------------

return CanvasItemManager