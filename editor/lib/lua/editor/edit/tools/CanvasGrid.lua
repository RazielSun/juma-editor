local ScriptProp = require("core.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type CanvasGrid
--
---------------------------------------------------------------------------------

local CanvasGrid = Class( ScriptProp, "CanvasGrid" )

function CanvasGrid:init( layer )
	self.layer = layer
	self.width = 1024
	self.height = 1024
	self.scale = 1
	self.x = 0
	self.y = 0
	self.deckSize = { self.width, self.height }
	ScriptProp.init(self)

	self.layer:insertProp( self._prop )
	self:attach()
end

---------------------------------------------------------------------------------
function CanvasGrid:onDraw()
	MOAIGfxDevice.setPenWidth( 1 )
	MOAIGfxDevice.setPenColor( .2, .2, .2, 1 )

	MOAIDraw.drawLine( 0, 100, 0, -100 )
	MOAIDraw.drawLine( 100, 0, -100, 0 )
end

---------------------------------------------------------------------------------
function CanvasGrid:setViewSize( width, height )
	self.width = width
	self.height = height
end

function CanvasGrid:setScale( scale )
	self.scale = scale
end

function CanvasGrid:setPos( x, y )
	self.x, self.y = x, y
end

---------------------------------------------------------------------------------

return CanvasGrid