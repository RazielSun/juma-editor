
local CoreNavigate = require("canvas.CanvasNavigate")

---------------------------------------------------------------------------------
--
-- @type CanvasNavigate
--
---------------------------------------------------------------------------------

local CanvasNavigate = Class( CoreNavigate, "Canvas3DNavigate" )

function CanvasNavigate:init( option )
	self.option = option
	option.name = option.name or "CanvasNavigate"

	self.rotating = false

	CoreNavigate.init( self, option )
end

---------------------------------------------------------------------------------
function CanvasNavigate:moveCameraToSelected()
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
function CanvasNavigate:startRotate( btn, x, y )
	self.rotateFrom = { x, y }
	self.cameraRot = { self.targetCamera:getRot() }
	self.rotating = btn
	self.entity:getScene():setCursor( 'cross' )
end

function CanvasNavigate:stopRotate()
	self.rotating = false
	self.entity:getScene():setCursor( 'arrow' )
end

---------------------------------------------------------------------------------
function CanvasNavigate:updateZoom()
	local zoom = self:getZoom()
	self.targetCamera:setScl( 1/zoom, 1/zoom, 1 ) -- todo: fixme
	self:updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasNavigate:onMouseDown( btn, wx, wy )
	if btn == 'right' then
		if self.dragging or self.rotating then return end
		if self.inputDevice:isKeyDown( 'space' ) then
			self:startDrag( btn, wx, wy )
		else
			self:startRotate( btn, wx, wy )
		end
	end
end

function CanvasNavigate:onMouseUp( btn, wx, wy )
	if btn == self.dragging then
		self:stopDrag()
	elseif btn == self.rotating then
		self:stopRotate()
	end
end

function CanvasNavigate:onMouseMove( wx, wy )
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

function CanvasNavigate:onMouseScroll( x, y )
	if self.dragging or self.rotating then return end

	if y > 0 then
		self:setZoom( self.zoom + 0.02 )
	else
		self:setZoom( self.zoom - 0.02 )
	end
end

---------------------------------------------------------------------------------

return CanvasNavigate
