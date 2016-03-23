
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
end

function CanvasToolManager:addLayer( layer )
	self.layer = layer
	self.underlay = {}
	layer:setUnderlayTable( self.underlay )
end

---------------------------------------------------------------------------------
function CanvasToolManager:setTool( id )
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
		self.tools[ prevTool.id ] = prevTool
		table.removeElement( self.underlay, prevTool.onDraw )
	end

	if toolClass then
		tool = toolClass( id )
	else
		return
	end

	assert( tool, "Canvas tool not be null!")

	self.activeTool = tool
	self:updateCanvas()
end

function CanvasToolManager:updateCanvas()
	if self.activeTool then
		table.push( self.underlay, self.activeTool.onDraw )
	end	
end

---------------------------------------------------------------------------------
function CanvasToolManager:onSelectionChanged( selection )
	if self.activeTool then
		self.activeTool:onSelectionChanged( selection )
	end
end

---------------------------------------------------------------------------------

return CanvasToolManager