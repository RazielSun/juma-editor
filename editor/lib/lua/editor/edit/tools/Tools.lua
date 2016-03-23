---------------------------------------------------------------------------------
--
-- @type CanvasTool
--
---------------------------------------------------------------------------------

local CanvasTool = Class( "CanvasTool" )

function CanvasTool:init( id )
	self.id = id
end

function CanvasTool:onDraw()
	print("onDraw CanvasTool")
end

function CanvasTool:onSelectionChanged( selection )
	--
end

---------------------------------------------------------------------------------
--
-- @type TransformTool
--
---------------------------------------------------------------------------------

local TransformTool = Class( CanvasTool, "TransformTool" )

function TransformTool:init( id )
	CanvasTool.init(self, id)
end

function TransformTool:onDraw()
	applyColor 'handle-all'
	MOAIDraw.fillRect( 0, 0, 0.5, 0.5 )
end

---------------------------------------------------------------------------------
--
-- @type RotateTool
--
---------------------------------------------------------------------------------

local RotateTool = Class( CanvasTool, "RotateTool" )

function RotateTool:init( id )
	CanvasTool.init(self, id)
end

function RotateTool:onDraw()
	applyColor 'handle-x'
	MOAIDraw.drawCircle( 0, 0, 0.5 )
end

---------------------------------------------------------------------------------
--
-- @type ScaleTool
--
---------------------------------------------------------------------------------

local ScaleTool = Class( CanvasTool, "ScaleTool" )

function ScaleTool:init( id )
	CanvasTool.init(self, id)
end

function ScaleTool:onDraw()
	applyColor 'handle-y'
	MOAIDraw.drawCircle( 0, 0, 0.3 )
end

---------------------------------------------------------------------------------

registerCanvasTool( 'move_object', TransformTool )
registerCanvasTool( 'rotate_object', RotateTool )
registerCanvasTool( 'scale_object', ScaleTool )

return {
	CanvasTool = CanvasTool,
	TransformTool = TransformTool,
	RotateTool = RotateTool,
	ScaleTool = ScaleTool,
}