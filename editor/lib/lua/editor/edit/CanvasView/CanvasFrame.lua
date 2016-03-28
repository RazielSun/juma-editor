
local ScriptProp = require("ui.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type CanvasFrame
--
---------------------------------------------------------------------------------

local CanvasFrame = Class( ScriptProp, "CanvasFrame" )

function CanvasFrame:init()
	self.FLAG_EDITOR_OBJECT = true
	self.deckSize = { 1024, 1024 }
	self.frameWidth = 320
	self.frameHeight = 480
	ScriptProp.init(self)
end

---------------------------------------------------------------------------------
function CanvasFrame:onLoad()
	self.layer:insertProp( self._prop )
	self:attach()
end

function CanvasFrame:onDraw()
	applyColor 'background-frame'
	local w, h = self.frameWidth, self.frameHeight

	MOAIGfxDevice.setPenWidth( 2 )
	MOAIDraw.drawRect( -w*0.5, -h*0.5, w*0.5, h*0.5 )

	MOAIGfxDevice.setPenWidth( 1 )
	MOAIDraw.drawLine( 0, -h*0.5, 0, h*0.5 )
	MOAIDraw.drawLine( -w*0.5, 0, w*0.5, 0 )
end

---------------------------------------------------------------------------------
function CanvasFrame:resize( width, height )
	self.frameWidth = width or 320
	self.frameHeight = height or 480
end

---------------------------------------------------------------------------------

return CanvasFrame