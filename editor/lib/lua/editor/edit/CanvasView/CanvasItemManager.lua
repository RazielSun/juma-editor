
local EditorEntity = require("edit.EditorEntity")
local InputEvent = require("input.InputEvent")

---------------------------------------------------------------------------------
--
-- @type CanvasItemManager
--
---------------------------------------------------------------------------------

local CanvasItemManager = Class( EditorEntity, "CanvasItemManager" )

function CanvasItemManager:init()
	self.items = {}
	self.activeItem = nil
	self.activeMouseButton = nil

	EditorEntity.init(self)
end

function CanvasItemManager:onLoad()
	assert( self.layer )
	local inputDevice = self:getView():getInputDevice()
	inputDevice:addMouseListener( self.onMouseEvent, self )
end

function CanvasItemManager:getView()
	return self.parent
end

---------------------------------------------------------------------------------
function CanvasItemManager:addItem( item )
	table.insert( self.items, 1, item )
	self:addChild( item )
end

function CanvasItemManager:removeItem( item )
	if table.removeElement( self.items, item ) then
		self:removeChild( item )
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
function CanvasItemManager:onMouseEvent( event )
	if event.eventName == InputEvent.DOWN then
		self:onMouseDown( event.touchId, event.x, event.y )
	elseif event.eventName == InputEvent.UP then
		self:onMouseUp( event.touchId, event.x, event.y )
	elseif event.eventName == InputEvent.MOVE then
		self:onMouseMove( event.x, event.y )
	end
end

function CanvasItemManager:onMouseDown( btn, x, y )
	if self.activeItem then return end
	local item = self:findTopItem( x, y )
	if item then
		self.activeItem = item
		self.activeItem:onMouseDown( btn, x, y )
		self.activeMouseButton = btn	
	end
	-- self:focus( item )
end

function CanvasItemManager:onMouseUp( btn, x, y )
	if self.activeMouseButton == btn then
		self.activeItem:onMouseUp( btn, x, y )
		self.activeMouseButton = false
		self.activeItem = false
	end
end

function CanvasItemManager:onMouseMove( x, y )
	if self.activeMouseButton then
		self.activeItem:onMouseMove( x, y )
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

	


---------------------------------------------------------------------------------

return CanvasItemManager