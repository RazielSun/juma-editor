
local InputEvent = require("input.InputEvent")

local CACHE_TOOLS = {}

function registerCanvasTool( id, clazz )
	CACHE_TOOLS[ id ] = clazz
end

---------------------------------------------------------------------------------
--
-- @type CanvasToolManager
--
---------------------------------------------------------------------------------

local CanvasToolManager = Class( "CanvasToolManager" )

function CanvasToolManager:init()
	self.tools = {}
	self.toolId = nil
	self.layer = MOAILayer.new()
end

---------------------------------------------------------------------------------
function CanvasToolManager:setTool( id )
	self.toolId = id
	
	local toolClass = nil
	local tool = nil
	if self.tools[ id ] then
		tool = self.tools[ id ]
		self.tools[ id ] = nil
	else
		toolClass = CACHE_TOOLS[ id ]
	end

	local prevTool = self.activeTool
	if prevTool then
		self.activeTool = nil
		self.tools[ prevTool.id ] = prevTool
		prevTool:stop()
	end

	if not tool then
		if toolClass then
			tool = toolClass( id, self.layer )
		else
			return
		end
	end

	assert( tool, "Canvas tool not be null!")

	self.activeTool = tool
	self:updateCanvas()
end

function CanvasToolManager:updateCanvas()
	if self.activeTool then
		self.activeTool:start()
	end
end

function CanvasToolManager:onMouseEvent( event )
	local intercept = false
	local tool = self.activeTool
	
	if tool and tool.target then
		if tool:inside( event.x, event.y ) and event.type == InputEvent.MOUSE_DOWN then
			tool:onMouseDown( event.x, event.y, event.btn )
			return true
		end

		if event.type == InputEvent.MOUSE_UP then
			tool:onMouseUp( event.x, event.y, event.btn )
		elseif event.type == InputEvent.MOUSE_MOVE then
			tool:onDrag( event.x, event.y, event.btn )
		end
		return true
	end
	return false
end

---------------------------------------------------------------------------------
function CanvasToolManager:onSelectionChanged( selection )
	if self.activeTool then
		self.activeTool:onSelectionChanged( selection )
	end
end

---------------------------------------------------------------------------------

return CanvasToolManager