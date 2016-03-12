require("KeyMap")

RenderContext = require("RenderContext")
Bridge = require("Bridge")

Editor = {}

--------------------------------------------------------------------
-- Context Related
--------------------------------------------------------------------
function Editor.setRenderStack( context, bufferTable, renderTableMap )
	if RenderContext then
		print("setRenderStack:", context, bufferTable, renderTableMap)
		local renderContext = RenderContext.getRenderContext( context )
		assert( renderContext, 'render context not found:' .. context )
		renderContext.renderTableMap    = renderTableMap
		renderContext.bufferTable       = bufferTable
	elseif context ~= 'game' then
		print( 'no RenderContext module found for render context functions')
	end

	if context == Editor.currentRenderContext then
		-- for framebuffer, renderTable in pairs( renderTableMap ) do
		-- 	-- framebuffer = bufferTable[i]
		-- 	-- print("keys:", framebuffer, renderTable )
		-- 	framebuffer:setRenderTable( renderTable )
		-- end
		MOAIRenderMgr.setBufferTable( bufferTable )
		MOAIRenderMgr.setRenderTable( renderTableMap )	
	end
end

function Editor.setCurrentRenderContext( key )
	Editor.currentRenderContext = key or 'game'
end

function Editor.getCurrentRenderContext()
	return Editor.currentRenderContext or 'game'
end

--------------------------------------------------------------------
local function onContextChange( ctx, oldCtx )
	Editor.setCurrentRenderContext( ctx )
end

RenderContext.addContextChangeListeners( onContextChange )
