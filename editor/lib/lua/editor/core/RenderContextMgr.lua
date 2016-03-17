--------------------------------------------------------------------
-- RENDER CONTEXT MGR
--------------------------------------------------------------------

local RenderContextMgr = {}

RenderContextMgr.contexts 	= {}
RenderContextMgr.current    = nil
RenderContextMgr.currentKey = nil

--------------------------------------------------------------------
--
function RenderContextMgr.createRenderContext( key, cr, cg, cb, ca )
	if RenderContextMgr then
		RenderContextMgr:create( key, cr, cg, cb, ca )
	end
end

function RenderContextMgr:create( key, cr, cg, cb, ca )
	if self.contexts[ key ] then
		return
	end

	if cr==0 and cg == 0 and cb == 0 and ca == 0 then
		cr, cg, cb, ca = nil, nil, nil, nil
	end

	local root = MOAIAction.new()
	root:setAutoStop( false )
	root._contextKey = key

	local frameBuffer = MOAIFrameBuffer.new()
	frameBuffer:setClearColor( cr or 0.06, cg or 0.06, cb or 0.06, ca or 1.0 )
	local context = {
		key              = key,
		w                = false,
		h                = false,
		actionRoot       = root,
		bufferTable      = { frameBuffer },
	}

	self.contexts[ key ] = context
end

function RenderContextMgr.changeRenderContext( key, w, h )
	if RenderContextMgr then
		RenderContextMgr:change( key, w, h )
	end
end

function RenderContextMgr:change( key, w, h )
	if self.currentKey == key then return end

	local context = self:get(key)
	assert ( context, 'no render context for:'..tostring(key) )

	self.current    = context
	self.currentKey = key
	self.current.w  = w
	self.current.h  = h

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

--------------------------------------------------------------------
--

function RenderContextMgr:pushCurrentRenderTable( renderTable )
	self:pushRenderTable( self.currentKey, renderTable )
end

function RenderContextMgr:pushRenderTable( key, renderTable )
	local context = self:get( key )
	if context then
		local frameBuffer = context.bufferTable[#context.bufferTable]
		if not frameBuffer then
			frameBuffer = MOAIFrameBuffer.new()
			table.insert( context.bufferTable, frameBuffer )
		end
		frameBuffer:setRenderTable( renderTable )
	end
end

--------------------------------------------------------------------
--

function RenderContextMgr.setBufferSize( width, height )
	RenderContextMgr:setBufferSizeForContext( RenderContextMgr.currentKey, width, height )
end

function RenderContextMgr:setBufferSizeForContext( key, width, height )
	local context = self:get( key )
	if context then
		local bufferTable = context.bufferTable
		setBufferSizeForTable( bufferTable, width, height )
	end
end

--------------------------------------------------------------------
--

function RenderContextMgr.manualRender()
	RenderContextMgr:manualRenderForContext( RenderContextMgr.currentKey )
end

function RenderContextMgr:manualRenderForContext( key )
	local context = self:get( key )
	if context then
		local bufferTable = context.bufferTable
		renderTable( bufferTable )
	end
end

return RenderContextMgr