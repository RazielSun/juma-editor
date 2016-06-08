
local CoreNavigate = require("canvas.CanvasNavigate")

---------------------------------------------------------------------------------
--
-- @type CanvasLookAtObject
--
---------------------------------------------------------------------------------

local CanvasLookAtObject = Class( CoreNavigate, "CanvasLookAtObject" )

function CanvasLookAtObject:init( option )
	self.option = option
	option.name = option.name or "CanvasLookAtObject"

	CoreNavigate.init( self, option )
end

---------------------------------------------------------------------------------
function CanvasLookAtObject:initOther()
	self.alpha = 0
	self.beta = math.pi/2
	self:updateCameraPos( self.alpha, self.beta )
end

---------------------------------------------------------------------------------
function CanvasLookAtObject:startDrag( btn, x, y )
	self.dragFrom = { x, y }
	self.cameraLoc = { self.targetCamera:getLoc() }
	self.dragging = btn
	self.entity:getScene():setCursor( 'cross' )
end

function CanvasLookAtObject:stopDrag( x, y )
	self.dragging = false

	local a, b = self:getAngles( x, y )
	self.alpha = a
	self.beta = b

	self:updateCameraPos( a, b )
	self.entity:getScene():setCursor( 'arrow' )
end

---------------------------------------------------------------------------------
function CanvasLookAtObject:getAngles( wx, wy )
	local x0, y0 = unpack( self.dragFrom )
	local dx, dy = wx - x0, wy - y0
	local factor = 0.01
	local a = self.alpha + dx * factor
	local b = self.beta + dy * factor
	b = math.clamp( b, 0, math.pi )
	return a, b
end

function CanvasLookAtObject:updateCameraPos( a, b )
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
function CanvasLookAtObject:onMouseDown( btn, wx, wy )
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

function CanvasLookAtObject:onMouseUp( btn, wx, wy )
	if btn == self.dragging then
		self:stopDrag( wx, wy )
	end
end

function CanvasLookAtObject:onMouseMove( wx, wy )
	if not self.dragging then return end
	local a, b = self:getAngles( wx, wy )
	self:updateCameraPos( a, b )
end

---------------------------------------------------------------------------------

return CanvasLookAtObject
