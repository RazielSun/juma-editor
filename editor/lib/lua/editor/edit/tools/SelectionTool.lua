
local CanvasTool = require("edit.tools.CanvasTool")
local CanvasPickPlane = require("edit.tools.CanvasPickPlane")

---------------------------------------------------------------------------------
--
-- @type SelectionTool
--
---------------------------------------------------------------------------------

local SelectionTool = Class( CanvasTool, "SelectionTool" )

function SelectionTool:init()
	CanvasTool.init(self)
end

function SelectionTool:onLoad()
	self:updateSelection()
end

function SelectionTool:updateSelection()
	self:clear()

	if not self.handle then
		local plane = CanvasPickPlane()
		local inputDevice = self.parent:getView():getInputDevice()
		plane:setPickCallback( function( picked )
			if inputDevice:isCtrlDown() then
				toggleSelection( 'scene', unpack( picked ) )
			elseif inputDevice:isShiftDown() then
				addSelection( 'scene', unpack( picked ) )
			elseif inputDevice:isAltDown() then
				removeSelection( 'scene', unpack( picked ) )
			else
				changeSelection( 'scene', unpack( picked ) )
			end
		end )
		self.handle = plane
	end

	self:addCanvasItem( self.handle )
end

function SelectionTool:clear()
	if self.handle then
		self:removeCanvasItem( self.handle )
	end
end

---------------------------------------------------------------------------------

return SelectionTool