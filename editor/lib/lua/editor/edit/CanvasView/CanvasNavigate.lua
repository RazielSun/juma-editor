
local EditorComponent = require("edit.EditorComponent")
local InputEvent = require("input.InputEvent")

local function _cameraZoomControlNodeCallback( node )
	return node.navigate:updateZoom()
end

---------------------------------------------------------------------------------
--
-- @type CanvasNavigate
--
---------------------------------------------------------------------------------

local CanvasNavigate = Class( EditorComponent, "CanvasNavigate" )

function CanvasNavigate:init( option )
	self.option = option
	option.name = option.name or "CanvasNavigate"

	EditorComponent.init( self, option )
end

---------------------------------------------------------------------------------
function CanvasNavigate:onLoad()
	local option = self.option or {}
	local inputDevice = option.inputDevice
	self.targetCamera = option.camera

	assert( inputDevice )
	inputDevice:addListener( self )
	self.inputDevice = inputDevice

	--zoom control
	self.zoomControlNode = MOAIScriptNode.new()
	self.zoomControlNode:reserveAttrs( 1 )
	self.zoomControlNode.navigate = self
	self:setZoom( 1 )
	self.zoomControlNode:setCallback( _cameraZoomControlNodeCallback )

	self.dragging = false
end

---------------------------------------------------------------------------------
function CanvasNavigate:moveCameraToSelected()
	local selection = getSelection( 'scene' )
	local target = selection[1]
	if target then
		local prop = nil
		if target.getProp then
			prop = target:getProp()
		else
			local com = target:findMethod( "getProp" )
			if com then
				prop = com:getProp()
			end
		end
		
		if prop then
			self.targetCamera:setLoc( prop:getLoc() )
		end	
	end
end

---------------------------------------------------------------------------------
function CanvasNavigate:startDrag( btn, x, y )
	self.dragFrom = { x, y }
	self.cameraFrom = { self.targetCamera:getLoc() }
	self.dragging = btn
	self.entity:getScene():setCursor( 'closed-hand' )
end

function CanvasNavigate:stopDrag()
	self.dragging = false
	self.entity:getScene():setCursor( 'arrow' )
end

function CanvasNavigate:getZoom()
	return self.zoomControlNode:getAttr( 1 )
end

function CanvasNavigate:setZoom( zoom )
	zoom = math.clamp( zoom, 1 / 16, 16 )
	self.zoom = zoom
	self.zoomControlNode:setAttr( 1, zoom or 1 )
	self.zoomControlNode:forceUpdate()
end

function CanvasNavigate:updateZoom()
	local zoom = self:getZoom()
	self.targetCamera:setScl( 1/zoom, 1/zoom, 1 )
	self:updateCanvas()
end

function CanvasNavigate:getView()
	return self.entity
end

function CanvasNavigate:updateCanvas()
	self:getView():updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasNavigate:onInputEvent( event )
	if event.id == InputEvent.MOUSE_EVENT then
		self:onMouseEvent( event )
	end
end

function CanvasNavigate:onMouseEvent( event )
	if event.eventName == InputEvent.DOWN then
		self:onMouseDown( event.idx, event.wx, event.wy )
	elseif event.eventName == InputEvent.UP then
		self:onMouseUp( event.idx, event.wx, event.wy )
	elseif event.eventName == InputEvent.MOVE then
		self:onMouseMove( event.wx, event.wy )
	elseif event.eventName == InputEvent.MOUSE_SCROLL then
		self:onMouseScroll( event.wx, event.wy )
	end
end

function CanvasNavigate:onMouseDown( btn, wx, wy )
	if btn == 'right' then
		if self.dragging then return end
		self:startDrag( btn, wx, wy )

	elseif btn == 'left' then
		if self.dragging then return end
		if self.inputDevice:isKeyDown( 'space' ) then
			self:startDrag( btn, wx, wy )
		end
	end
end

function CanvasNavigate:onMouseUp( btn, wx, wy )
	if btn == self.dragging then
		self:stopDrag()
	end
end

function CanvasNavigate:onMouseMove( wx, wy )
	if not self.dragging then return end
	local x0, y0 = unpack( self.dragFrom )
	local dx, dy = wx - x0, wy - y0
	local cx0, cy0 = unpack( self.cameraFrom )

	local zoom = self.zoom
	self.targetCamera:setLoc( cx0 - dx/zoom, cy0 + dy/zoom, 0 )

	self:updateCanvas()
end

function CanvasNavigate:onMouseScroll( x, y )
	if self.dragging then return end

	if y > 0 then
		self:setZoom( self.zoom + 0.02 )
	else
		self:setZoom( self.zoom - 0.02 )
	end
end

---------------------------------------------------------------------------------

return CanvasNavigate