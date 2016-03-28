
local ScriptProp = require("ui.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type CanvasItem
--
---------------------------------------------------------------------------------

local CanvasItem = Class( ScriptProp, "CanvasItem" )

function CanvasItem:init()
	self.FLAG_EDITOR_OBJECT = true
	ScriptProp.init(self)
end

function CanvasItem:getView()
	return self.parent:getView()
end

---------------------------------------------------------------------------------
function CanvasItem:setTarget( target )
	self.target = target
	self:getProp():setAttrLink ( MOAITransform.INHERIT_TRANSFORM, target:getProp(), MOAITransform.TRANSFORM_TRAIT )
end

---------------------------------------------------------------------------------
function CanvasItem:wndToWorld( wx, wy )
	local x, y = self.layer:wndToWorld( wx or 0, wy or 0, 0 )
	return x, y
end

function CanvasItem:wndToModel( wx, wy )
	local mx, my = self:worldToModel( self:wndToWorld( wx, wy ) )
	return mx, my
end

---------------------------------------------------------------------------------

return CanvasItem