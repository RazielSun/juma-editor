--------------------------------------------------------------------
-- RENDER CONTEXT
--------------------------------------------------------------------

local RenderContext = {}

local renderContextTable = {}
--[[
	RenderContext incluces:
		1. an action root
		2. a render table
	shares:
		layer information
		prop
		assets
]]

local currentContext    = false
local currentContextKey = false

local ContextChangeListeners = {}

function RenderContext.addContextChangeListeners( f )
	ContextChangeListeners[ f ] = true
end

function RenderContext.removeContextChangeListener( f )
	ContextChangeListeners[ f ] = nil
end

function RenderContext.createRenderContext( key, cr,cg,cb,ca )
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
	renderContextTable[ key ] = context
end

function RenderContext.changeRenderContext( key, w, h )
	if currentContextKey == key then return end
	local context = renderContextTable[key]
	print("changeRenderContext:", currentContextKey, key, w, h)
	assert ( context, 'no render context for:'..tostring(key) )
	for f in pairs( ContextChangeListeners ) do
		f( key, currentContextKey )
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

	local clearColor = currentContext.clearColor
	if clearColor then 
		MOAIGfxDevice.getFrameBuffer():setClearColor( unpack( clearColor ) )
	else
		MOAIGfxDevice.getFrameBuffer():setClearColor( )
	end

	-- for fb, rt in pairs( currentContext.renderTableMap ) do
	-- 	fb:setRenderTable( rt )
	-- end
	-- MOAIRenderMgr.setBufferTable ( currentContext.bufferTable )	
	-- if currentContext.deviceRenderTable then
	-- 	deviceBuffer:setRenderTable  ( currentContext.deviceRenderTable )
	-- end
	MOAIRenderMgr.setRenderTable ( currentContext.renderTableMap )
	MOAIActionMgr.setRoot        ( currentContext.actionRoot )
end

function RenderContext.getCurrentRenderContextKey()
	return currentContextKey
end

function RenderContext.getCurrentRenderContext()
	return currentContext
end

function RenderContext.getRenderContext( key )
	return renderContextTable[ key ]
end

function RenderContext.setCurrentRenderContextActionRoot( root )
	currentContext.actionRoot = root
	MOAIActionMgr.setRoot( root )
end

function RenderContext.setRenderContextActionRoot( key, root )
	local context =  getRenderContext( key )
	if key == currentContextKey then
		MOAIActionMgr.setRoot( root )
	end
	if context then
		context.actionRoot = root
	end
end

return RenderContext