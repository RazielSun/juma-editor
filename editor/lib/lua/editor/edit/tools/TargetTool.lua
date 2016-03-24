
---------------------------------------------------------------------------------
--
-- @type TargetTool
--
---------------------------------------------------------------------------------

local TargetTool = Class( "TargetTool" )

function TargetTool:init( id, layer )
	self.id = id
	self.layer = layer
	self.target = nil
end

---------------------------------------------------------------------------------
function TargetTool:start()
end

function TargetTool:stop()
end

function TargetTool:inside( x, y )
	return false
end

function TargetTool:onSelectionChanged( selection )
end

function TargetTool:onMouseDown( x, y, btn )
end

function TargetTool:onMouseUp( x, y, btn )
end

function TargetTool:onDrag( x, y, btn )
end

---------------------------------------------------------------------------------

registerCanvasTool( 'select_object', TargetTool )

return TargetTool