
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
	self.activeItem = item
	self.items[ item ] = true
	self:addChild( item )
end

function CanvasItemManager:removeItem( item )
	self.activeItem = nil
	self.items[ item ] = nil
	self:removeChild( item )
end

---------------------------------------------------------------------------------
function CanvasItemManager:onMouseEvent( event )
	local item = self.activeItem
	local success = false
	if item then
		if event.eventName == InputEvent.DOWN then
			if item.onMouseDown then success = item:onMouseDown( event.touchId, event.x, event.y ) end
		elseif event.eventName == InputEvent.UP then
			if item.onMouseUp then success = item:onMouseUp( event.touchId, event.x, event.y ) end
		elseif event.eventName == InputEvent.MOVE then
			if item.onMouseMove then success = item:onMouseMove( event.x, event.y ) end
		end
	end
end

---------------------------------------------------------------------------------

return CanvasItemManager