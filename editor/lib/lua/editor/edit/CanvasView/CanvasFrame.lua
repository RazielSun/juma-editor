
local ScriptProp = require("ui.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type CanvasFrame
--
---------------------------------------------------------------------------------

local CanvasFrame = Class( ScriptProp, "CanvasFrame" )

function CanvasFrame:init( option )
	option = option or {}
	self.FLAG_EDITOR_OBJECT = true
	self.deckSize = { 1024, 1024 }
	self.ui = option.ui

	assert( self.ui )

	self.frameWidth, self.frameHeight = self.ui:getSize()
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

	MOAIGfxDevice.setPenWidth( 3 )
	MOAIDraw.drawRect( -w*0.5, -h*0.5, w*0.5, h*0.5 )
end

---------------------------------------------------------------------------------
function CanvasFrame:resize( width, height )
	self.frameWidth = width or 320
	self.frameHeight = height or 480
	self.ui:setSize( width, height )
end

---------------------------------------------------------------------------------

return CanvasFrame