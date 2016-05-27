
local ScriptPropComponent = require("entity.components.ScriptPropComponent")

---------------------------------------------------------------------------------
--
-- @type Canvas3DDrawGrid
--
---------------------------------------------------------------------------------

local Canvas3DDrawGrid = Class( ScriptPropComponent, "Canvas3DDrawGrid" )

function Canvas3DDrawGrid:init()
	self.FLAG_EDITOR_OBJECT = true

	self.visible = true
	self.deckSize = { 1000, 1000 } --{ 20000, 20000 }
	self.gridSize = { 100, 100 }

	ScriptPropComponent.init(self, { name = "Canvas3DDrawGrid" })
end

---------------------------------------------------------------------------------
function Canvas3DDrawGrid:onLoad()
	self.layer = self.entity.layer
	assert( self.layer )

	local prop = self:getProp()
	prop:setRot( 90, 0, 0 )
	self.layer:insertProp( prop )
	self:attach()
end

function Canvas3DDrawGrid:onDraw()
	local w, h = unpack(self.deckSize)
	local x0, y1 = -w*0.5, h*0.5
	local x1, y0 = w*0.5, -h*0.5

	MOAIGfxDevice.setPenWidth( 1 )
	
	local dx = x1-x0
	local dy = y1-y0
	local gw, gh = unpack(self.gridSize)
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

return Canvas3DDrawGrid
