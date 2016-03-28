
local CanvasItem = require("edit.tools.CanvasItem")

local itemSize = 80
local itemArrowSize = 16
local itemPad = 15

---------------------------------------------------------------------------------
--
-- @type TranslationItem
--
---------------------------------------------------------------------------------

local TranslationItem = Class( CanvasItem, "TranslationItem" )

function TranslationItem:init()
	CanvasItem.init(self)
	self:attach()
end

function TranslationItem:onDraw()
	MOAIGfxDevice.setPenWidth(1)
	applyColor 'handle-all'
	MOAIDraw.fillRect( 0,0, itemArrowSize, itemArrowSize )
	--x axis
	applyColor 'handle-x'
	MOAIDraw.drawLine( 0,0, itemSize, 0 )
	MOAIDraw.fillFan(
		itemSize,  itemArrowSize/3, 
		itemSize + itemArrowSize, 0,
		itemSize, -itemArrowSize/3
		)
	--y axis
	applyColor 'handle-y'
	MOAIDraw.drawLine( 0,0, 0, itemSize )
	MOAIDraw.fillFan(
		itemArrowSize/3, itemSize, 
		0, itemSize + itemArrowSize,
		-itemArrowSize/3, itemSize 
		)
end

function TranslationItem:inside( x, y )
	return self:calcActiveAxis( x, y ) ~= false
end

function TranslationItem:calcActiveAxis( x, y )
	local x, y = self:wndToModel( x, y )
	if x >= 0 and y >= 0 and x <= itemArrowSize + itemPad and y <= itemArrowSize + itemPad then
		return 'all'
	elseif math.abs( y ) < itemPad and x <= itemSize + itemArrowSize and x > -itemPad then
		return 'x'
	elseif math.abs( x ) < itemPad and y <= itemSize + itemArrowSize and y > -itemPad then
		return 'y'
	end
	return false
end

function TranslationItem:onMouseDown( btn, x, y )
	if btn~='left' then return end

	self.activeAxis = false
	self.x0, self.y0 = self:wndToWorld( x, y )

	target = self.target
	target:forceUpdate()
	local tx, ty = target:getLoc()
	self.tx0, self.ty0 = tx, ty

	self.activeAxis = self:calcActiveAxis( x, y )
	if self.activeAxis then
		self.target:preTransform()
		return true
	end
end

function TranslationItem:onMouseUp( btn, x, y )
	if btn~='left' then return end
	if not self.activeAxis then return end
	self.activeAxis = false
	return true
end

function TranslationItem:onMouseMove( x, y )
	if not self.activeAxis then return end

	local target = self.target
	target:forceUpdate()
	self:forceUpdate()
	x, y = self:wndToWorld( x, y )
	local dx = x - self.x0
	local dy = y - self.y0

	local tx0, ty0 = self.tx0, self.ty0
	local tx, ty = tx0 + dx, ty0 + dy

	-- tx, ty = self:getView():snapLoc( tx, ty, nil, self.activeAxis )
	if self.activeAxis == 'all' then
		-- pass
	elseif self.activeAxis == 'x' then
		ty = ty0
	elseif self.activeAxis == 'y' then
		tx = tx0
	end
	target:setLoc( tx, ty )
	self.tool:updateCanvas()
	return true
end

function TranslationItem:onArrowsPressed( key, down, shift )
	if not down then return end

	local x, y, z = 0, 0, 0
	local step = shift and 10 or 1
	if key == "down" then
		y = -step
	elseif key == "up" then
		y = step
	elseif key == "left" then
		x = -step
	elseif key == "right" then
		x = step
	end

	local target = self.target
	target:forceUpdate()
	self:forceUpdate()

	local tx, ty, tz = target:getLoc()
	target:setLoc( tx+x, ty+y, tz+z )
	self.tool:updateCanvas()
end

---------------------------------------------------------------------------------
--
-- @type RotateItem
--
---------------------------------------------------------------------------------

local RotateItem = Class( CanvasItem, "RotateItem" )

function RotateItem:init()
	CanvasItem.init(self)
	self.align  = false
	self.active = false
	self:attach()
end

function RotateItem:getRotZ()
	return self:getProp():getAttr( MOAITransform.ATTR_Z_ROT )
end

function RotateItem:onDraw()
	MOAIGfxDevice.setPenWidth(1)
	if self.active then
		applyColor 'handle-active'
	else
		applyColor 'handle-z'
	end
	MOAIDraw.fillCircle( 0, 0, 5 )
	MOAIDraw.drawCircle( 0, 0, itemSize )
	local r = self:getRotZ()	
	MOAIDraw.drawLine( 0,0, math.vecAngle( r, itemSize ) )
	if self.active then
		MOAIGfxDevice.setPenWidth(2)
		applyColor 'handle-previous'
		MOAIDraw.drawLine( 0,0, math.vecAngle( self.r0, itemSize ) )
	end
end

function RotateItem:inside( x, y )
	local x, y = self:wndToModel( x, y )
	local r = math.distance( 0, 0, x, y )
	return r <= itemSize
end

function RotateItem:onMouseDown( btn, x, y )
	if btn~='left' then return end
	
	local x1, y1 = self:wndToModel( x, y )
	local rx, ry, rz = self.target:getRot()
	self.rot0 = rz
	self.dir0 = math.direction( 0,0, x1,y1 )
	self.active = true
	self.target:preTransform()	
	self.r0 = self:getRotZ()
	self.tool:updateCanvas()
	return true
end

function RotateItem:onMouseUp( btn, x, y )
	if btn~='left' then return end
	if not self.active then return end
	self.active = false
	self.tool:updateCanvas()
	return true
end

function RotateItem:onMouseMove( x, y )
	if not self.active then return end
	local x1, y1 = self:wndToModel( x, y )
	local r = math.distance( 0,0, x1,y1 )
	if r > 5 then
		local dir = math.direction( 0,0, x1,y1 )
		local ddir = dir - self.dir0
		local rx,ry,rz = self.target:getRot()
		rz = self.rot0 + ddir * 180/math.pi
		self.target:setRot( rx, ry, rz )
		-- emitPythonSignal( 'entity.modified', self.target, 'view' )
		self.tool:updateCanvas()
		return true
	end
end

---------------------------------------------------------------------------------
--
-- @type ScaleItem
--
---------------------------------------------------------------------------------

local ScaleItem = Class( CanvasItem, "ScaleItem" )

function ScaleItem:init()
	CanvasItem.init(self)
	self:attach()
end

function ScaleItem:onDraw()
	MOAIGfxDevice.setPenWidth(1)
	applyColor 'handle-all'
	MOAIDraw.fillRect( 0, 0, itemArrowSize, itemArrowSize )
	--x axis
	applyColor 'handle-x'
	MOAIDraw.drawLine( 0, 0, itemSize, 0 )
	MOAIDraw.fillRect( itemSize,0, itemSize + itemArrowSize, itemArrowSize )
	--y axis
	applyColor 'handle-y'
	MOAIDraw.drawLine( 0, 0, 0, itemSize )
	MOAIDraw.fillRect( 0, itemSize, itemArrowSize, itemSize + itemArrowSize )
end


function ScaleItem:inside( x, y )
	return self:calcActiveAxis( x, y ) ~= false
end

function ScaleItem:calcActiveAxis( x, y )
	local x, y = self:wndToModel( x, y )
	if x >= 0 and y >= 0 and x <= itemArrowSize + itemPad and y <= itemArrowSize + itemPad then
		return 'all'
	elseif math.abs( y ) < itemPad and x <= itemSize + itemArrowSize and x > -itemPad then
		return 'x'
	elseif math.abs( x ) < itemPad and y <= itemSize + itemArrowSize and y > -itemPad then
		return 'y'
	end
	return false
end

function ScaleItem:onMouseDown( btn, x, y)
	if btn~='left' then return end	
	self.x0 = x
	self.y0 = y
	self.activeAxis = self:calcActiveAxis( x, y )
	self.sx, self.sy, self.sz = self.target:getScl()
	if self.activeAxis then
		self.target:preTransform()
		return true
	end
end

function ScaleItem:onMouseUp( btn, x, y )
	if btn~='left' then return end
	if not self.activeAxis then return end
	self.activeAxis = false
	return true
end

function ScaleItem:onMouseMove( x, y )
	if not self.activeAxis then return end
	local target = self.target
	target:forceUpdate()
	self:forceUpdate()
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
	-- emitPythonSignal( 'entity.modified', self.target, 'view' )
	self.tool:updateCanvas()
	return true
end

---------------------------------------------------------------------------------

local SelectionTool = require("edit.tools.SelectionTool")
local TransformToolHelper = require("edit.tools.TransformToolHelper")

---------------------------------------------------------------------------------
--
-- @type TransformTool
--
---------------------------------------------------------------------------------

local TransformTool = Class( SelectionTool, "TransformTool" )

function TransformTool:init()
	SelectionTool.init(self)
end

function TransformTool:onLoad()
	self:updateSelection()
end

function TransformTool:onSelectionChanged( selection )
	self:updateSelection()
end

function TransformTool:updateSelection()
	local selection = self:getSelection()
	local entities = {}
	local count = 0

	for i, e in ipairs( selection ) do
		entities[ e ] = true
		count = count + 1
	end

	if count == 0 then entities = nil end

	self:clear()
	self.target = false

	if not self.handle then
		self.handle = self:createHandle()
		self.handle.tool = self
	end

	local top = self:findTopLevelEntities( entities )
	if top then
		self:addCanvasItem( self.handle )
		local target = TransformToolHelper()
		target:setTargets( top )
		self.target = target
		self:updateHandleTarget( target )
	end
	self:updateCanvas()
end

function TransformTool:createHandle() -- virtual
end

function TransformTool:updateHandleTarget( target ) -- virtual
end

function TransformTool:clear()
	if self.handle then
		self:removeCanvasItem( self.handle )
	end
end

---------------------------------------------------------------------------------
--
-- @type TranslationTool
--
---------------------------------------------------------------------------------

local TranslationTool = Class( TransformTool, "TranslationTool" )

function TranslationTool:createHandle()
	local handle = TranslationItem()
	return handle
end

function TranslationTool:updateHandleTarget( target )
	target:setUpdateMasks( true, false, false )
	self.handle:setTarget( target )
end

---------------------------------------------------------------------------------
--
-- @type RotationTool
--
---------------------------------------------------------------------------------

local RotationTool = Class( TransformTool, "RotationTool" )

function RotationTool:createHandle()
	local handle = RotateItem()
	return handle
end

function RotationTool:updateHandleTarget( target )
	if target.targetCount > 1 then
		target:setUpdateMasks( true, true, false )
	else
		target:setUpdateMasks( false, true, false )
	end
	self.handle:setTarget( target )
end

---------------------------------------------------------------------------------
--
-- @type ScaleTool
--
---------------------------------------------------------------------------------

local ScaleTool = Class( TransformTool, "ScaleTool" )

function ScaleTool:createHandle()
	local handle = ScaleItem()
	return handle
end

function ScaleTool:updateHandleTarget( target )
	if target.targetCount > 1 then
		target:setUpdateMasks( false, true, true )
	else
		target:setUpdateMasks( false, false, true )
	end
	self.handle:setTarget( target )
end

---------------------------------------------------------------------------------

registerCanvasTool( 'translation', TranslationTool )
registerCanvasTool( 'rotation',    RotationTool    )
registerCanvasTool( 'scale',       ScaleTool       )
