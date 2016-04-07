
local ScriptPropComponent = require("entity.components.ScriptPropComponent")

---------------------------------------------------------------------------------
--
-- @type CanvasItem
--
---------------------------------------------------------------------------------

local CanvasItem = Class( ScriptPropComponent, "CanvasItem" )

function CanvasItem:init()
	self.FLAG_EDITOR_OBJECT = true
	ScriptPropComponent.init(self, { name = "CanvasItem" })
end

function CanvasItem:getView()
	return self.parent:getView()
end

---------------------------------------------------------------------------------
function CanvasItem:setTarget( target )
	self.target = target
	self:getProp():setAttrLink ( MOAITransform.INHERIT_TRANSFORM, target:getProp(), MOAITransform.TRANSFORM_TRAIT )
end

function CanvasItem:inside( x, y, z, pad )
	return true
end

---------------------------------------------------------------------------------
function CanvasItem:wndToModel( wx, wy )
	local mx, my = self:worldToModel( self:wndToWorld( wx, wy ) )
	return mx, my
end

---------------------------------------------------------------------------------

return CanvasItem