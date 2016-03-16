--------------------------------------------------------------------
-- RENDER CONTEXT MGR
--------------------------------------------------------------------

local RenderContextMgr = Class( "RenderContextMgr" )

assert(CTHelper.setBufferSize, "CTHelper setBufferSize is NULL")
assert(CTHelper.renderFrameBuffer, "CTHelper renderFrameBuffer is NULL")

--------------------------------------------------------------------
--
function RenderContextMgr:init( params )
	self.contexts = {}
	self.current    = nil
	self.currentKey = nil
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
	if self.currentKey == key then return end

	local context = self.contexts[key]
	assert ( context, 'no render context for:'..tostring(key) )

	-- local deviceBuffer = MOAIGfxDevice.getFrameBuffer()

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

	self.current    = context
	self.currentKey = key
	self.current.w  = w
	self.current.h  = h

	-- local clearColor = currentContext.clearColor
	-- if clearColor then 
	-- 	MOAIGfxDevice.getFrameBuffer():setClearColor( unpack( clearColor ) )
	-- else
	-- 	MOAIGfxDevice.getFrameBuffer():setClearColor()
	-- end

	for fb, rt in pairs( self.current.renderTableMap ) do
		fb:setRenderTable( rt )
	end
	-- MOAIRenderMgr.setBufferTable ( self.current.bufferTable )	
	-- if currentContext.deviceRenderTable then
	-- 	deviceBuffer:setRenderTable  ( currentContext.deviceRenderTable )
	-- end
	-- MOAIActionMgr.setRoot( self.current.actionRoot )
end

function RenderContextMgr:getCurrentContextKey()
	return self.currentKey
end

function RenderContextMgr:getCurrentContext()
	return self.current
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

function RenderContextMgr:updateCurrentContext( bufferTable )
	local context = self.current

	if context then
		context.bufferTable = bufferTable
	end
end

--------------------------------------------------------------------
--

local setBufferSize = CTHelper.setBufferSize

local function setBufferSizeForTable( t, width, height )
	for _, item in ipairs(t) do
		local itemType = type(item)
		if itemType == 'table' then
			setBufferSizeForTable( item, width, height )
		elseif itemType == 'userdata' then
			setBufferSize( item, width, height )
		end
	end
end

function RenderContextMgr:setBufferSizeForCurrent( width, height )
	local context = self.current

	if context then
		local bufferTable = context.bufferTable
		setBufferSizeForTable( bufferTable, width, height )
	end
end

--------------------------------------------------------------------
--

local renderFrameBuffer = CTHelper.renderFrameBuffer

local function renderTable( t )
	for _, item in ipairs(t) do
		local itemType = type(item)
		if itemType == 'table' then
			renderTable( item )
		elseif itemType == 'userdata' then
			renderFrameBuffer( item )
		end
	end
end

function RenderContextMgr:manualRenderAll()
	-- local bufferTable = MOAIRenderMgr.getBufferTable()

	-- if bufferTable then
	-- 	renderTable( bufferTable )
	-- else
	-- 	renderFrameBuffer(MOAIGfxDevice.getFrameBuffer())
	-- end
	local context = self.current

	if context then
		local bufferTable = context.bufferTable
		renderTable( bufferTable )
	end
end

return RenderContextMgr