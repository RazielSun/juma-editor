require("KeyMap")

RenderContext = require("RenderContext")

Game = {}

--------------------------------------------------------------------
--Context Related
--------------------------------------------------------------------
function Game.setRenderStack( context, bufferTable, renderTableMap )
	if RenderContext then
		print("setRenderStack:", context, bufferTable, renderTableMap)
		local renderContext = RenderContext.getRenderContext( context )
		assert( renderContext, 'render context not found:' .. context )
		renderContext.renderTableMap    = renderTableMap
		renderContext.bufferTable       = bufferTable
	elseif context ~= 'game' then
		print( 'no RenderContext module found for render context functions')
	end

	if context == Game.currentRenderContext then
		-- for i, renderTable in ipairs( renderTableMap ) do
		-- 	framebuffer = bufferTable[i]
		-- 	print("keys:", framebuffer, renderTable )
		-- 	framebuffer:setRenderTable( renderTable )		
		-- end
		-- MOAIRenderMgr.setBufferTable( bufferTable )
		MOAIRenderMgr.setRenderTable( renderTableMap )	
	end
end

function Game.setCurrentRenderContext( key )
	Game.currentRenderContext = key or 'game'
end

function Game.getCurrentRenderContext()
	return Game.currentRenderContext or 'game'
end

--------------------------------------------------------------------
local function onContextChange( ctx, oldCtx )
	Game.setCurrentRenderContext( ctx )
end

RenderContext.addContextChangeListeners( onContextChange )
