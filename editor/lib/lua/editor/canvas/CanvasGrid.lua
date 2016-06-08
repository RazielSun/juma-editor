
local ScriptPropComponent = require("entity.components.ScriptPropComponent")

---------------------------------------------------------------------------------
--
-- @type CanvasGrid
--
---------------------------------------------------------------------------------

local CanvasGrid = Class( ScriptPropComponent, "CanvasGrid" )

function CanvasGrid:init()
	self.FLAG_EDITOR_OBJECT = true

	self.visible = true
	self.deckSize = { 20000, 20000 }
	self.viewSize = { 0, 0 }
	self.gridSize = { 100, 100 }

	ScriptPropComponent.init(self, { name = "CanvasGrid" })
end

---------------------------------------------------------------------------------
function CanvasGrid:onLoad()
	local layer = self.entity.layer
	assert(layer)

	self:setLayer( layer )
	
	self:attach()
end

function CanvasGrid:onDraw()
	local w, h = unpack(self.viewSize)
	local x0, y1 = self:wndToWorld( 0, 0 )
	local x1, y0 = self:wndToWorld( w, h )

	if w==0 or h==0 then
		x0, y0 = -100000, -100000
		x1, y1 = 100000, 100000
	else
		applyColor 'grid'
		MOAIGfxDevice.setPenWidth( 1 )
		local dx = x1-x0
		local dy = y1-y0
		local gw, gh = unpack(self.gridSize)
		local col = math.ceil( dx/gw )
		local row = math.ceil( dy/gh )
		local cx0 = math.floor( x0/gw ) * gw
		local cy0 = math.floor( y0/gh ) * gh
		for x = cx0, cx0 + col*gw, gw do
			MOAIDraw.drawLine( x, y0, x, y1 )
		end
		for y = cy0, cy0 + row*gh, gh do
			MOAIDraw.drawLine( x0, y, x1, y )
		end
	end

	--Axis
	applyColor 'grid-zero'
	MOAIGfxDevice.setPenWidth( 1 )
	MOAIDraw.drawLine( x0, 0, x1, 0 )
	MOAIDraw.drawLine( 0, y0, 0, y1 )
end

---------------------------------------------------------------------------------
function CanvasGrid:resizeView( width, height )
	self.viewSize = { width or 0, height or 0 }
end

---------------------------------------------------------------------------------

return CanvasGrid

-- function CanvasGrid:getWidth()
-- 	return self.gridSize[1]
-- end

-- function CanvasGrid:getHeight()
-- 	return self.gridSize[2]
-- end

-- function CanvasGrid:setWidth( w )
-- 	self:setSize( w, self:getHeight() )
-- end

-- function CanvasGrid:setHeight( h )
-- 	self:setSize( self:getWidth(), h )
-- end

-- function CanvasGrid:setSize( w, h )
-- 	self.gridSize = { w, h }
-- end

-- function CanvasGrid:getSize()
-- 	return self.gridSize[1], self.gridSize[2]
-- end

