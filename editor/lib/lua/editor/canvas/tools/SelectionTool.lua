
local CanvasTool = require("canvas.tools.CanvasTool")
local CanvasPickPlane = require("canvas.tools.CanvasPickPlane")

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
	local plane = self:addCanvasItem( CanvasPickPlane() )
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
	self.plane = plane
end

---------------------------------------------------------------------------------

return SelectionTool