
local EditorComponent = require("edit.EditorComponent")
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

local CanvasToolManager = Class( EditorComponent, "CanvasToolManager" )

function CanvasToolManager:init()
	self.tools = {}
	self.activeTool = nil
	EditorComponent.init(self, { name = "CanvasToolManager"})
end

function CanvasToolManager:getView()
	return self:getEntity()
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
		self.tools[ prevTool.__toolId ] = prevTool
		prevTool:clear()
	end

	if not tool then
		if toolClass then
			tool = toolClass()
			tool.parent = self
		else
			return
		end
	end

	assert( tool, "Canvas tool not be null!")

	tool.__toolId = id
	self.activeTool = tool
	self.activeTool:updateSelection()
end

---------------------------------------------------------------------------------
function CanvasToolManager:onSelectionChanged( selection )
	if self.activeTool then
		self.activeTool:onSelectionChanged( selection )
	end
end

---------------------------------------------------------------------------------

return CanvasToolManager
