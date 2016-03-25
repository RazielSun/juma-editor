local ScriptProp = require("ui.ScriptProp")

---------------------------------------------------------------------------------
--
-- @type CanvasTool
--
---------------------------------------------------------------------------------

local CanvasTool = Class( ScriptProp, "CanvasTool" )

function CanvasTool:init( id, layer )
	self.id = id
	self.layer = layer
	self.size = 80
	self.arrowSize = 16
	self.pad = 15
	self.lineWidth = 1
	self.target = nil

	ScriptProp.init(self)
end

function CanvasTool:start()
	self.layer:insertProp( self._prop )
	self:updateSelection()
end

function CanvasTool:stop()
	self.layer:removeProp( self._prop )
	self:setTarget( nil )
end

function CanvasTool:setTarget( target )
	self.target = target
	self._prop:setVisible( target ~= nil )
	if target then
		self._prop:setAttrLink ( MOAITransform.INHERIT_LOC, target:getProp(), MOAITransform.TRANSFORM_TRAIT )
	else
		self._prop:clearAttrLink ( MOAITransform.INHERIT_LOC )
	end
end

function CanvasTool:inside( x, y )
	return false
end

function CanvasTool:wndToWorld( wx, wy )
	local x, y = self.layer:wndToWorld( wx or 0, wy or 0, 0 )
	return x, y
end

function CanvasTool:wndToModel( wx, wy )
	local x, y = self:wndToWorld( wx, wy )
	local mx, my = self._prop:worldToModel( x, y, 0 )
	return mx, my
end

function CanvasTool:onDraw()
end

function CanvasTool:getSelection( key )
	return getSelection( key or 'scene' )
end

function CanvasTool:updateSelection()
	local selection = self:getSelection()

	if selection and #selection > 0 then
		local target = selection[1]
		if target ~= self.target then
			self:setTarget( target )
		end
	else
		self:setTarget( nil )
	end
end

function CanvasTool:onSelectionChanged( selection )
	self:updateSelection()
end

function CanvasTool:onMouseDown( x, y, btn )
end

function CanvasTool:onMouseUp( x, y, btn )
end

function CanvasTool:onDrag( x, y, btn )
end

---------------------------------------------------------------------------------
--
-- @type TransformTool
--
---------------------------------------------------------------------------------

local TransformTool = Class( CanvasTool, "TransformTool" )

function TransformTool:init( id, layer )
	CanvasTool.init(self, id, layer)
	self:attach()
end

function TransformTool:onDraw()
	MOAIGfxDevice.setPenWidth(self.lineWidth)
	applyColor 'handle-all'
	MOAIDraw.fillRect( 0,0, self.arrowSize, self.arrowSize )
	--x axis
	applyColor 'handle-x'
	MOAIDraw.drawLine( 0,0, self.size, 0 )
	MOAIDraw.fillFan(
		self.size,  self.arrowSize/3, 
		self.size + self.arrowSize, 0,
		self.size, -self.arrowSize/3
		)
	--y axis
	applyColor 'handle-y'
	MOAIDraw.drawLine( 0,0, 0, self.size )
	MOAIDraw.fillFan(
		self.arrowSize/3, self.size, 
		0, self.size + self.arrowSize,
		-self.arrowSize/3, self.size 
		)
end

function TransformTool:inside( x, y )
	return self:calcActiveAxis( x, y ) ~= false
end

function TransformTool:calcActiveAxis( x, y )
	local x, y = self:wndToModel( x, y )
	if x >= 0 and y >= 0 and x <= self.arrowSize + self.pad and y <= self.arrowSize + self.pad then
		return 'all'
	elseif math.abs( y ) < self.pad and x <= self.size + self.arrowSize and x > -self.pad then
		return 'x'
	elseif math.abs( x ) < self.pad and y <= self.size + self.arrowSize and y > -self.pad then
		return 'y'
	end
	return false
end

function TransformTool:onMouseDown( x, y, btn )
	if btn~='left' then return end

	self.activeAxis = false
	self.x0, self.y0 = self:wndToWorld( x, y )

	target = self.target
	-- target:forceUpdate()
	local tx, ty = target:getLoc()
	self.tx0, self.ty0 = tx, ty

	self.activeAxis = self:calcActiveAxis( x, y )
	if self.activeAxis then
		-- self.target:preTransform()
	end
end

function TransformTool:onMouseUp( x, y, btn )
	if btn~='left' then return end
	if not self.activeAxis then return end
	self.activeAxis = false
end

function TransformTool:onDrag( x, y, btn )
	if not self.activeAxis then return end

	local target = self.target
	-- target:forceUpdate()
	-- self:forceUpdate()
	x, y = self:wndToWorld( x, y )
	local dx = x - self.x0
	local dy = y - self.y0

	local tx0, ty0 = self.tx0, self.ty0
	local tx, ty = tx0 + dx, ty0 + dy

	-- tx, ty = self:getView():snapLoc( tx, ty, nil, self.activeAxis )
	if self.activeAxis == 'all' then -- pass
	elseif self.activeAxis == 'x' then
		ty = ty0
	elseif self.activeAxis == 'y' then
		tx = tx0
	end
	target:setLoc( tx, ty )
	emitPythonSignal( 'entity.modified', self.target, 'view' )
	-- self.tool:updateCanvas()
end

---------------------------------------------------------------------------------
--
-- @type RotateTool
--
---------------------------------------------------------------------------------

local RotateTool = Class( CanvasTool, "RotateTool" )

function RotateTool:init( id, layer )
	CanvasTool.init(self, id, layer)
	self.align  = false
	self.active = false
	self.lineWidth = 2
	self:attach()
end

function RotateTool:getRotZ()
	if not self.target then return 0 end
	local _, _, z = self.target:getRot()
	return z
end

function RotateTool:onDraw()
	MOAIGfxDevice.setPenWidth(self.lineWidth)
	if self.active then
		applyColor 'handle-active'
	else
		applyColor 'handle-z'
	end
	MOAIDraw.fillCircle( 0, 0, 5 )
	MOAIDraw.drawCircle( 0, 0, self.size )
	local r = self:getRotZ()	
	MOAIDraw.drawLine( 0,0, math.vecAngle( r, self.size ) )
	if self.active then
		applyColor 'handle-previous'
		MOAIDraw.drawLine( 0,0, math.vecAngle( self.r0, self.size ) )
	end
end

function RotateTool:inside( x, y )
	local x, y = self:wndToModel( x, y )
	local r = math.distance( 0, 0, x, y )
	return r <= self.size
end

function RotateTool:onMouseDown( x, y, btn )
	if btn~='left' then return end
	
	local x1, y1 = self:wndToModel( x, y )
	local rx, ry, rz = self.target:getRot()
	self.rot0 = rz
	self.dir0 = math.direction( 0,0, x1,y1 )
	self.active = true
	-- self.target:preTransform()	
	self.r0 = self:getRotZ()
	-- self.tool:updateCanvas()
end

function RotateTool:onMouseUp( x, y, btn )
	if btn~='left' then return end
	if not self.active then return end
	self.active = false
	-- self.tool:updateCanvas()
end

function RotateTool:onDrag( x, y, btn )
	if not self.active then return end
	local x1, y1 = self:wndToModel( x, y )
	local r = math.distance( 0,0, x1,y1 )
	if r > 5 then
		local dir = math.direction( 0,0, x1,y1 )
		local ddir = dir - self.dir0
		local rx,ry,rz = self.target:getRot()
		rz = self.rot0 + ddir * 180/math.pi
		self.target:setRot( rx, ry, rz )
		emitPythonSignal( 'entity.modified', self.target, 'view' )
		-- self.tool:updateCanvas()
	end
end


---------------------------------------------------------------------------------
--
-- @type ScaleTool
--
---------------------------------------------------------------------------------

local ScaleTool = Class( CanvasTool, "ScaleTool" )

function ScaleTool:init( id, layer )
	CanvasTool.init(self, id, layer)
	self:attach()
end

function ScaleTool:onDraw()
	MOAIGfxDevice.setPenWidth(self.lineWidth)
	applyColor 'handle-all'
	MOAIDraw.fillRect( 0, 0, self.arrowSize, self.arrowSize )
	--x axis
	applyColor 'handle-x'
	MOAIDraw.drawLine( 0, 0, self.size, 0 )
	MOAIDraw.fillRect( self.size,0, self.size + self.arrowSize, self.arrowSize )
	--y axis
	applyColor 'handle-y'
	MOAIDraw.drawLine( 0, 0, 0, self.size )
	MOAIDraw.fillRect( 0, self.size, self.arrowSize, self.size + self.arrowSize )
end

function ScaleTool:inside( x, y )
	return self:calcActiveAxis( x, y ) ~= false
end

function ScaleTool:calcActiveAxis( x, y )
	local x, y = self:wndToModel( x, y )
	if x >= 0 and y >= 0 and x <= self.arrowSize + self.pad and y <= self.arrowSize + self.pad then
		return 'all'
	elseif math.abs( y ) < self.pad and x <= self.size + self.arrowSize and x > -self.pad then
		return 'x'
	elseif math.abs( x ) < self.pad and y <= self.size + self.arrowSize and y > -self.pad then
		return 'y'
	end
	return false
end

function ScaleTool:onMouseDown( x, y, btn )
	if btn~='left' then return end	
	self.x0 = x
	self.y0 = y
	self.activeAxis = self:calcActiveAxis( x, y )
	self.sx, self.sy, self.sz = self.target:getScl()
	if self.activeAxis then
		-- self.target:preTransform()
	end
end

function ScaleTool:onMouseUp( x, y, btn )
	if btn~='left' then return end
	if not self.activeAxis then return end
	self.activeAxis = false
end

function ScaleTool:onDrag( x, y, btn )
	if not self.activeAxis then return end
	local target = self.target
	-- target:forceUpdate()
	-- self:forceUpdate()
	local dx = x - self.x0
	local dy = y - self.y0

	if self.activeAxis == 'all' then
		local k = 1 + math.magnitude( dx, dy ) / 100 * math.sign(dx) 
		self.target:setScl( 
			self.sx * k,
			self.sy * k,
			self.sz * 1 )
	elseif self.activeAxis == 'x' then
		local k = 1 + math.magnitude( dx, 0 ) / 100 * math.sign(dx) 
		self.target:setScl( 
			self.sx * k,
			self.sy * 1,
			self.sz * 1 )

	elseif self.activeAxis == 'y' then
		local k = 1 - math.magnitude( dy, 0 ) / 100 * math.sign(dy) 
		self.target:setScl( 
			self.sx * 1,
			self.sy * k,
			self.sz * 1 )
	end
	emitPythonSignal( 'entity.modified', self.target, 'view' )
	-- self.tool:updateCanvas()	
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