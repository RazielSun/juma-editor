
---------------------------------------------------------------------------------
--
-- @type DragCameraTool
--
---------------------------------------------------------------------------------

local DragCameraTool = Class( "DragCameraTool" )

function DragCameraTool:init( id, layer )
	self.id = id
	self.layer = layer
	self.target = nil
end

function DragCameraTool:setTargetLayer( targetLayer )
	self.targetLayer = targetLayer
end

---------------------------------------------------------------------------------
function DragCameraTool:start()
	self:updateSelection()
end

function DragCameraTool:stop()
	self:setTarget( nil )
end

function DragCameraTool:setTarget( target )
	self.target = target
end

function DragCameraTool:inside( x, y )
	return true
end

function DragCameraTool:updateSelection()
	local target = self.targetLayer:getCamera()
	if target ~= self.target then
		self:setTarget( target )
	end
end

function DragCameraTool:onSelectionChanged( selection )
	self:updateSelection()
end

function DragCameraTool:onMouseDown( x, y, btn )
	if btn~='left' then return end
	self.active = true
	self.x0, self.y0 = x, y

	target = self.target
	local tx, ty = target:getLoc()
	self.tx0, self.ty0 = tx, ty
end

function DragCameraTool:onMouseUp( x, y, btn )
	if btn~='left' then return end
	if not self.active then return end
	self.active = false
end

function DragCameraTool:onDrag( x, y, btn )
	if not self.active then return end

	local dx, dy = self.x0 - x, y - self.y0
	local tx0, ty0 = self.tx0, self.ty0
	local tx, ty = tx0 + dx, ty0 + dy

	local target = self.target
	target:setLoc( tx, ty )
end

---------------------------------------------------------------------------------

registerCanvasTool( 'drag_camera', DragCameraTool )

return DragCameraTool