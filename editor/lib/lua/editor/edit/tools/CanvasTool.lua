
local EditorEntity = require("edit.EditorEntity")
local InputEvent = require("input.InputEvent")

---------------------------------------------------------------------------------
--
-- @type CanvasTool
--
---------------------------------------------------------------------------------

local CanvasTool = Class( EditorEntity, "CanvasTool" )

function CanvasTool:init()
	EditorEntity.init(self, {name="CanvasTool"})
	self.items = {}
end

function CanvasTool:onLoad()
end

function CanvasTool:clear()
end

function CanvasTool:getCurrentView()
	return self.parent:getView()
end

function CanvasTool:updateCanvas()
	self:getCurrentView():updateCanvas()
end

---------------------------------------------------------------------------------
function CanvasTool:installInput( inputDevice )
	assert( inputDevice )
	self.inputDevice = inputDevice
end

function CanvasTool:getInput()
	return self.inputDevice
end

---------------------------------------------------------------------------------
function CanvasTool:addCanvasItem( item )
	local view = self:getCurrentView()
	view:addCanvasItem( item )
	self.items[ item ] = true
	item.tool = self
	return item
end

function CanvasTool:removeCanvasItem( item )
	local view = self:getCurrentView()
	view:removeCanvasItem( item )
	self.items[ item ] = nil
	item.tool = nil
	return item
end

---------------------------------------------------------------------------------
function CanvasTool:findTopLevelPropComponents( entities )
	local found = {}
	if not entities then
		return false
	end

	for e in pairs( entities ) do
		local p = e.parent
		local isTop = true
		while p do
			if entities[ p ] then
				isTop = false
				break
			end
			p = p.parent
		end
		
		if isTop and e.getProp then
			found[e] = true
		end
	end

	return found
end

---------------------------------------------------------------------------------
function CanvasTool:getSelection( key )
	return getSelection( key or 'scene' )
end

function CanvasTool:updateSelection()
end

---------------------------------------------------------------------------------
function CanvasTool:onSelectionChanged( selection )
	self:updateSelection()
end

---------------------------------------------------------------------------------

return CanvasTool