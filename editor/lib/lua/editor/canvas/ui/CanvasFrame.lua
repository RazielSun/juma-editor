
local ScriptPropComponent = require("entity.components.ScriptPropComponent")

---------------------------------------------------------------------------------
--
-- @type CanvasFrame
--
---------------------------------------------------------------------------------

local CanvasFrame = Class( ScriptPropComponent, "CanvasFrame" )

function CanvasFrame:init( option )
	local option = option or {}
	option.name = option.name or "CanvasFrame"
	self.FLAG_EDITOR_OBJECT = true
	self.deckSize = { 2048, 2048 }

	self.ui = option.ui

	assert( self.ui )

	self.frameWidth, self.frameHeight = self.ui:getSize()
	ScriptPropComponent.init(self, option)
end

---------------------------------------------------------------------------------
function CanvasFrame:onLoad()
	local layer = self.entity.layer
	assert(layer)

	self:setLayer( layer )
	
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