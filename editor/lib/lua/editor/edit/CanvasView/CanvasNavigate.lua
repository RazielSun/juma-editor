
local EditorEntity = require("edit.EditorEntity")
local InputEvent = require("input.InputEvent")

---------------------------------------------------------------------------------
--
-- @type CanvasNavigate
--
---------------------------------------------------------------------------------

local CanvasNavigate = Class( EditorEntity, "CanvasNavigate" )

function CanvasNavigate:init( option )
	self.option = option
	EditorEntity.init( self, option )
end

---------------------------------------------------------------------------------
function CanvasNavigate:onLoad()
	local option = self.option or {}
	local inputDevice = option.inputDevice
	self.targetCamera = option.camera

	assert( inputDevice )
	inputDevice:addMouseListener( self.onMouseEvent, self )
	self.inputDevice = inputDevice
	self.zoom = 1
	self.dragging = false
end

---------------------------------------------------------------------------------
function CanvasNavigate:startDrag( btn, x, y )
	self.dragFrom = { x, y }
	self.cameraFrom = { self.targetCamera:getLoc() }
	self.dragging = btn
	self.parent:getScene():setCursor( 'closed-hand' )
end

function CanvasNavigate:stopDrag()
	self.dragging = false
	self.parent:getScene():setCursor( 'arrow' )
end

function CanvasNavigate:updateCanvas()
	self.parent:updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasNavigate:onMouseEvent( event )
	if event.eventName == InputEvent.DOWN then
		self:onMouseDown( event.touchId, event.x, event.y )
	elseif event.eventName == InputEvent.UP then
		self:onMouseUp( event.touchId, event.x, event.y )
	elseif event.eventName == InputEvent.MOVE then
		self:onMouseMove( event.x, event.y )
	end
end

function CanvasNavigate:onMouseDown( btn, x, y )
	if btn == 'right' then
		if self.dragging then return end
		self:startDrag( btn, x, y )

	elseif btn == 'left' then
		if self.dragging then return end
		if self.inputDevice:isKeyDown( 'space' ) then
			self:startDrag( btn, x, y )
		end
	end
end

function CanvasNavigate:onMouseUp( btn, x, y )
	if btn == self.dragging then
		self:stopDrag()
	end
end

function CanvasNavigate:onMouseMove( x, y )
	if not self.dragging then return end
	local x0, y0 = unpack( self.dragFrom )
	local dx, dy = x - x0, y - y0
	local cx0, cy0 = unpack( self.cameraFrom )
	-- local zoom = cameraCom:getZoom()
	-- local z0 = self.targetCamera:getLocZ()
	-- self.targetCamera:setLoc( cx0 - dx/zoom, cy0 + dy/zoom, z0 )
	self.targetCamera:setLoc( cx0 - dx, cy0 + dy, 0 )
	self:updateCanvas()
end

---------------------------------------------------------------------------------

return CanvasNavigate