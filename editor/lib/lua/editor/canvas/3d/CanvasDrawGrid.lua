
local ScriptPropComponent = require("entity.components.ScriptPropComponent")

---------------------------------------------------------------------------------
--
-- @type CanvasDrawGrid
--
---------------------------------------------------------------------------------

local CanvasDrawGrid = Class( ScriptPropComponent, "CanvasDrawGrid" )

function CanvasDrawGrid:init( option )
	self.FLAG_EDITOR_OBJECT = true

	local option = option or {}
	self.visible = true
	self.deckSize = option.deckSize or { 1000, 1000 }
	self.cellSize = option.cellSize or { 100, 100 }
	self.rotate = option.rotate or { 0, 0, 0 }

	ScriptPropComponent.init(self, { name = "CanvasDrawGrid" })
end

---------------------------------------------------------------------------------
function CanvasDrawGrid:onLoad()
	local layer = self.entity.layer
	assert( layer )

	self:getProp():setRot( unpack(self.rotate) )
	self:setLayer( layer )

	self:attach()
end

function CanvasDrawGrid:onDraw()
	local w, h = unpack(self.deckSize)
	local x0, y1 = -w*0.5, h*0.5
	local x1, y0 = w*0.5, -h*0.5

	MOAIGfxDevice.setPenWidth( 1 )
	
	local dx = x1-x0
	local dy = y1-y0
	local gw, gh = unpack(self.cellSize)
	local col = math.ceil( dx/gw )
	local row = math.ceil( dy/gh )
	local cx0 = math.floor( x0/gw ) * gw
	local cy0 = math.floor( y0/gh ) * gh

	applyColor 'grid'
	for x = cx0, cx0 + col*gw, gw do
		MOAIDraw.drawLine( x, y0, x, y1 )
	end
	for y = cy0, cy0 + row*gh, gh do
		MOAIDraw.drawLine( x0, y, x1, y )
	end

	--Axis
	applyColor 'grid-zero'
	MOAIDraw.drawLine( x0, 0, x1, 0 )
	MOAIDraw.drawLine( 0, y0, 0, y1 )
end

---------------------------------------------------------------------------------

return CanvasDrawGrid
