
local EditorComponent = require("core.EditorComponent")
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
	self.rotating = false
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:moveCameraToSelected()
	-- local selection = getSelection( 'scene' )
	-- local target = selection[1]
	-- if target then
	-- 	local prop = nil
	-- 	if target.getProp then
	-- 		prop = target:getProp()
	-- 	else
	-- 		local com = target:findMethod( "getProp" )
	-- 		if com then
	-- 			prop = com:getProp()
	-- 		end
	-- 	end
		
	-- 	if prop then
	-- 		self.targetCamera:setLoc( prop:getLoc() )
	-- 	end	
	-- end
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:startDrag( btn, x, y )
	self.dragFrom = { x, y }
	self.cameraLoc = { self.targetCamera:getLoc() }
	self.dragging = btn
	self.entity:getScene():setCursor( 'closed-hand' )
end

function Canvas3DNavigate:stopDrag()
	self.dragging = false
	self.entity:getScene():setCursor( 'arrow' )
end

---------------------------------------------------------------------------------
function Canvas3DNavigate:startRotate( btn, x, y )
	self.rotateFrom = { x, y }
	self.cameraRot = { self.targetCamera:getRot() }
	self.rotating = btn
	self.entity:getScene():setCursor( 'cross' )
end

function Canvas3DNavigate:stopRotate()
	self.rotating = false
	self.entity:getScene():setCursor( 'arrow' )
end

---------------------------------------------------------------------------------
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
	self.targetCamera:setScl( 1/zoom, 1/zoom, 1 ) -- todo: fixme
	self:updateCanvas()
end

function Canvas3DNavigate:getView()
	return self.entity
end

function Canvas3DNavigate:updateCanvas()
	self:getView():updateCanvas()
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
		if self.dragging or self.rotating then return end
		if self.inputDevice:isKeyDown( 'space' ) then
			self:startDrag( btn, wx, wy )
		else
			self:startRotate( btn, wx, wy )
		end
	end
end

function Canvas3DNavigate:onMouseUp( btn, wx, wy )
	if btn == self.dragging then
		self:stopDrag()
	elseif btn == self.rotating then
		self:stopRotate()
	end
end

function Canvas3DNavigate:onMouseMove( wx, wy )
	if not self.dragging and not self.rotating then return end

	if self.dragging then
		local x0, y0 = unpack( self.dragFrom )
		local dx, dy = wx - x0, wy - y0
		local cx0, cy0 = unpack( self.cameraLoc )
		local factor = self.inputDevice:isKeyDown( 'shift' ) and 10 or 1
		self.targetCamera:setLoc( cx0 - dx*factor, cy0 + dy*factor, 0 ) -- todo: fixme
	elseif self.rotating then
		local rx0, ry0 = unpack( self.rotateFrom )
		-- local dx, dy = wx - rx0
		-- todo: create rotate
	end

	self:updateCanvas()
end

function Canvas3DNavigate:onMouseScroll( x, y )
	if self.dragging or self.rotating then return end

	if y > 0 then
		self:setZoom( self.zoom + 0.02 )
	else
		self:setZoom( self.zoom - 0.02 )
	end
end

---------------------------------------------------------------------------------

return Canvas3DNavigate
