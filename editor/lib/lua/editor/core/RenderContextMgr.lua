--------------------------------------------------------------------
-- RENDER CONTEXT MGR
--------------------------------------------------------------------

local EventDispatcher = require("core.EventDispatcher")

local RenderContextMgr = Class( EventDispatcher, "RenderContextMgr" )

--------------------------------------------------------------------
--
function RenderContextMgr:init( params )
	EventDispatcher.init( self, params )

	self.contexts = {}
	self.current    = false
	self.currentKey = false
	self.listeners = {}
end

--------------------------------------------------------------------
--
function RenderContextMgr:addListener( f )
	self.listeners[ f ] = true
end

function RenderContextMgr:removeListener( f )
	self.listeners[ f ] = nil
end

--------------------------------------------------------------------
--
function RenderContextMgr:create( key, cr, cg, cb, ca )
	if self.contexts[ key ] then
		return
	end

	local clearColor = {0,0,0,1}
	if cr==false then
		clearColor = false
	else
		clearColor = { cr or 0, cg or 0, cb or 0, ca or 0 }
	end

	local root = MOAIAction.new()
	root:setAutoStop( false )
	root._contextKey = key

	local context = {
		key              = key,
		w                = false,
		h                = false,
		clearColor       = clearColor,
		actionRoot       = root,
		bufferTable      = {},
		renderTableMap   = {},
	}

	self.contexts[ key ] = context
end

function RenderContextMgr:change( key, w, h )
	if currentKey == key then return end
	local context = self.contexts[key]
	assert ( context, 'no render context for:'..tostring(key) )
	for f in pairs( self.listeners ) do
		f( key, currentKey )
	end

	local deviceBuffer = MOAIGfxDevice.getFrameBuffer()

	-- if currentContext then --persist context
	-- 	local bufferTable  = MOAIRenderMgr.getBufferTable()
	-- 	local renderTableMap = {}
	-- 	local hasDeviceBuffer = false
	-- 	for i, fb in pairs( bufferTable ) do
	-- 		if fb.getRenderTarget then
	-- 			renderTableMap[fb] = fb:getRenderTable()
	-- 		end
	-- 	end		
	-- 	currentContext.bufferTable       = bufferTable
	-- 	currentContext.renderTableMap    = renderTableMap

	-- 	if currentContext.deviceRenderTable ~= false then
	-- 		currentContext.deviceRenderTable = deviceBuffer:getRenderTable()
	-- 	end

	-- 	currentContext.actionRoot        = assert( currentContext.actionRoot )
	-- end

	--TODO: persist clear depth& color flag(need to modify moai)
	
	currentContext    = context
	currentContextKey = key
	currentContext.w  = w
	currentContext.h  = h

	-- local clearColor = currentContext.clearColor
	-- if clearColor then 
	-- 	MOAIGfxDevice.getFrameBuffer():setClearColor( unpack( clearColor ) )
	-- else
	-- 	MOAIGfxDevice.getFrameBuffer():setClearColor( )
	-- end

	-- for fb, rt in pairs( currentContext.renderTableMap ) do
	-- 	fb:setRenderTable( rt )
	-- end
	-- MOAIRenderMgr.setBufferTable ( currentContext.bufferTable )	
	-- if currentContext.deviceRenderTable then
	-- 	deviceBuffer:setRenderTable  ( currentContext.deviceRenderTable )
	-- end
	-- MOAIRenderMgr.setRenderTable ( currentContext.renderTableMap )
	-- MOAIActionMgr.setRoot        ( currentContext.actionRoot )
end

function RenderContextMgr:getCurrentKey()
	return currentContextKey
end

function RenderContextMgr:getCurrent()
	return currentContext
end

function RenderContextMgr:get( key )
	return self.contexts[ key ]
end

function RenderContextMgr:setCurrentActionRoot( root )
	self.current.actionRoot = root
	MOAIActionMgr.setRoot( root )
end

function RenderContextMgr:setActionRoot( key, root )
	local context =  self:get( key )
	if key == self.currentKey then
		MOAIActionMgr.setRoot( root )
	end
	if context then
		context.actionRoot = root
	end
end

return RenderContextMgr