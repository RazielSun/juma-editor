
local EditorComponent = require("edit.EditorComponent")
local InputEvent = require("input.InputEvent")

local function _cameraZoomControlNodeCallback( node )
	return node.navigate:updateZoom()
end

---------------------------------------------------------------------------------
--
-- @type Canvas3DNavigate
--
---------------------------------------------------------------------------------

local Canvas3DNavigate = Class( EditorComponent, "Canvas3DNavigate" )

function Canvas3DNavigate:init( option )
	self.option = option
	option.name = option.name or "Canvas3DNavigate"

	EditorComponent.init( self, option )
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:onLoad()
	local option = self.option or {}
	local inputDevice = option.inputDevice
	self.targetCamera = option.camera
	self.alpha = 0
	self.beta = math.pi/2
	self:updateCameraPos( self.alpha, self.beta )

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
function Canvas3DNavigate:startDrag( btn, x, y )
	self.dragFrom = { x, y }
	self.cameraFrom = { self.targetCamera:getLoc() }
	self.dragging = btn
	-- self.entity:getScene():setCursor( 'closed-hand' )
end

function Canvas3DNavigate:stopDrag( x, y )
	self.dragging = false

	local a, b = self:getAngles( x, y )
	self.alpha = a
	self.beta = b

	self:updateCameraPos( a, b )
	-- self.entity:getScene():setCursor( 'arrow' )
end


function Canvas3DNavigate:getZoom()
	return self.zoomControlNode:getAttr( 1 )
end

function Canvas3DNavigate:setZoom( zoom )
	zoom = math.clamp( zoom, 1 / 16, 16 )
	self.zoom = zoom
	self.zoomControlNode:setAttr( 1, zoom or 1 )
	self.zoomControlNode:forceUpdate()
end

function Canvas3DNavigate:updateZoom()
	local zoom = self:getZoom()
	self.targetCamera:setScl( 1/zoom, 1/zoom, 1 )
	self:updateCanvas()
end

function Canvas3DNavigate:getView()
	return self.entity
end

function Canvas3DNavigate:updateCanvas()
	self:getView():updateCanvas()
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:getAngles( wx, wy )
	local x0, y0 = unpack( self.dragFrom )
	local dx, dy = wx - x0, wy - y0
	local factor = 0.01
	local a = self.alpha + dx * factor
	local b = self.beta + dy * factor
	a = self:normalize( a )
	b = self:normalize( b )
	return a, b
end

function Canvas3DNavigate:normalize( angle )
	local angle = angle or 0
	if angle > 2*math.pi then angle = angle - math.pi*2
	elseif angle < -2*math.pi then angle = angle + math.pi*2
	end
	return angle
end

function Canvas3DNavigate:updateCameraPos( a, b )
	local x, y, z = 0, 0, 0
	local radius = 500
	x = math.sin(b) * math.sin(a) * radius
	z = math.sin(b) * math.cos(a) * radius
	y = math.cos(b) * radius

	-- print("move camera to", x, y, z, "angle:", a, b)
	local camera = self.targetCamera
	camera:setLoc( x, y, z )
	camera:lookAt( 0, 0, 0 )

	self:updateCanvas()
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:onInputEvent( event )
	if event.id == InputEvent.MOUSE_EVENT then
		self:onMouseEvent( event )
	end
end

function Canvas3DNavigate:onMouseEvent( event )
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

function Canvas3DNavigate:onMouseDown( btn, wx, wy )
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

function Canvas3DNavigate:onMouseUp( btn, wx, wy )
	if btn == self.dragging then
		self:stopDrag( wx, wy )
	end
end

function Canvas3DNavigate:onMouseMove( wx, wy )
	if not self.dragging then return end
	local a, b = self:getAngles( wx, wy )
	self:updateCameraPos( a, b )
end

function Canvas3DNavigate:onMouseScroll( x, y )
	if self.dragging then return end

	if y > 0 then
		self:setZoom( self.zoom + 0.02 )
	else
		self:setZoom( self.zoom - 0.02 )
	end
end

---------------------------------------------------------------------------------

return Canvas3DNavigate
