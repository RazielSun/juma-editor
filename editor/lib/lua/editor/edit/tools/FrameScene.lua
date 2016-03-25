local ScriptProp = require("ui.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type FrameScene
--
---------------------------------------------------------------------------------

local FrameScene = Class( ScriptProp, "FrameScene" )

function FrameScene:init( layer )
	self.layer = layer
	self.deckSize = { 1024, 1024 }
	self.frameWidth = 320
	self.frameHeight = 480
	ScriptProp.init(self)

	self.layer:insertProp( self._prop )
	self:attach()
end

---------------------------------------------------------------------------------
function FrameScene:onDraw()
	applyColor 'background-frame'
	-- MOAIGfxDevice.setPenWidth( 2 )
	-- MOAIGfxDevice.setPenColor( .4, .4, .4, .5 )

	local w, h = self.frameWidth, self.frameHeight
	MOAIDraw.fillRect( -w*0.5, -h*0.5, w*0.5, h*0.5 )
	-- MOAIDraw.drawLine( 0, 10, 0, -10 )
	-- MOAIDraw.drawLine( 10, 0, -10, 0 )
end

---------------------------------------------------------------------------------
function FrameScene:resize( width, height )
	self.frameWidth = width or 320
	self.frameHeight = height or 480
end

---------------------------------------------------------------------------------

return FrameScene