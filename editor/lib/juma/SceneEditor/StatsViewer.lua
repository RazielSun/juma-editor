function onStart()
	STATS = {}
	STATS.thread = MOAICoroutine.new()

	local nIdx = 0
	local node = {0}
	local action = {0}
	local sim = {0}
	local render = {0}
	local buffer = 10
	STATS.thread:run( function()
		while true do
			local _, a, n, s, r = MOAISim.getPerformance()
			nIdx = (nIdx + 1) % buffer
			action[nIdx + 1] = a
			node[nIdx + 1] = n
			sim[nIdx + 1] = s
			render[nIdx + 1] = r

			local nodeMgrTime = 0
			local actionTreeTime = 0
			local simTime = 0
			local renderTime = 0
			for i = 1, #action do
				nodeMgrTime = nodeMgrTime + node[i]
				actionTreeTime = actionTreeTime + action[i]
				simTime = simTime + sim[i]
				renderTime = renderTime + render[i]
			end
			STATS.nodeMgr = 1000 * nodeMgrTime / buffer
			STATS.actionTree = 1000 * actionTreeTime / buffer
			STATS.simTime = 1000 * simTime / buffer
			STATS.renderTime = 1000 * renderTime / buffer
			coroutine.yield()
		end
	end )
end

function onStats()
	local fps = MOAISim.getPerformance()
	local drawcalls = MOAIGfxDevice.getFrameBuffer():getPerformanceDrawCount()
	local luaCount = MOAISim.getLuaObjectCount()
	local mem = MOAISim.getMemoryUsage()
	local lua, texture = mem.lua, mem.texture
	local node = STATS and STATS.nodeMgr or 0
	local action = STATS and STATS.actionTree or 0
	local sim = STATS and STATS.simTime or 0
	local render = STATS and STATS.renderTime or 0
	return math.round(fps, 0.1), drawcalls, luaCount, lua, texture, 
	math.round(node, 0.01), math.round(action, 0.01), math.round(sim, 0.01), math.round(render, 0.01)
end

function onStop()
	if STATS and STATS.thread then
		STATS.thread:stop()
		STATS.thread = nil
	end
end