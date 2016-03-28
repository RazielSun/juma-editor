
local CanvasItem = require("edit.tools.CanvasItem")

---------------------------------------------------------------------------------
--
-- @type CanvasPickPlane
--
---------------------------------------------------------------------------------

local CanvasPickPlane = Class( CanvasItem, "CanvasPickPlane" )

function CanvasPickPlane:init()
	self.deckSize = { 20000, 20000 }
	CanvasItem.init(self)
	self.x0 = 0
	self.y0 = 0
	self.x1 = 0
	self.y1 = 0

	self.onPicked = false
	self.picking = false
end

function CanvasPickPlane:onLoad()
	self:attach()
	self:getProp():setBlendMode( MOAIProp.GL_SRC_ALPHA, MOAIProp.GL_ONE_MINUS_SRC_ALPHA ) 
end

function CanvasPickPlane:inside()
	return true
end

function CanvasPickPlane:onDraw()
	local x0 = self.x0
	local y0 = self.y0
	local x1 = self.x1
	local y1 = self.y1
	MOAIGfxDevice.setPenColor( 0, .68, 0.58, 0.2 )
	MOAIDraw.fillRect( x0,y0,x1,y1 )
	MOAIGfxDevice.setPenColor( 0, .68, 0.58, 1 )
	MOAIDraw.drawRect( x0,y0,x1,y1 )
end

function CanvasPickPlane:setPickCallback( cb )
	self.onPicked = cb
end

function CanvasPickPlane:isConstantSize()
	return false
end

---------------------------------------------------------------------------------
function CanvasPickPlane:onMouseDown( btn, x, y )
	if btn ~= 'left' then return end
	local view = self:getView()
	x, y = view:wndToWorld( x, y )
	self.x0 = x
	self.y0 = y
	self.x1 = x 
	self.y1 = y
	self.picking = true
	self:setVisible( true )	
	view:updateCanvas()
	return true
end

function CanvasPickPlane:onMouseMove( x, y )
	if not self.picking then return end
	local view = self:getView()
	x, y = view:wndToWorld( x, y )
	self.x1 = x
	self.y1 = y
	view:updateCanvas()
	return true
end

function CanvasPickPlane:onMouseUp( btn, x, y )
	if btn == 'left' and self.picking then
		self.picking = false
		self:setVisible( false )
		local view = self:getView()
		view:updateCanvas()

		local x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
		if math.distance(x0, y0, x1, y1) < 5 then
			local picked = view:pick( x1, y1 )
			if self.onPicked then
				return self.onPicked( picked )
			end
		else
			local picked = view:pickRect( x0, y0, x1, y1 )
			if self.onPicked then
				return self.onPicked( picked )
			end
		end
	end
end

---------------------------------------------------------------------------------

return CanvasPickPlane