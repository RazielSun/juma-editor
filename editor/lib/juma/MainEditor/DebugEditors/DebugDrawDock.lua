
local DEBUG_DRAW = {
	-- COLLISION_ACTIVE_PROP_BOUNDS = MOAIDebugLines.COLLISION_ACTIVE_PROP_BOUNDS,
	-- COLLISION_ACTIVE_OVERLAP_PROP_BOUNDS = MOAIDebugLines.COLLISION_ACTIVE_OVERLAP_PROP_BOUNDS,
	-- COLLISION_ACTIVE_TOUCHED_PROP_BOUNDS = MOAIDebugLines.COLLISION_ACTIVE_TOUCHED_PROP_BOUNDS,
	-- COLLISION_OVERLAP_PROP_BOUNDS = MOAIDebugLines.COLLISION_OVERLAP_PROP_BOUNDS,
	PARTITION_CELLS = MOAIDebugLines.PARTITION_CELLS,
	PARTITION_PADDED_CELLS = MOAIDebugLines.PARTITION_PADDED_CELLS,
	-- PROP_MODEL_AXIS = MOAIDebugLines.PROP_MODEL_AXIS,
	-- PROP_MODEL_DIAGONALS = MOAIDebugLines.PROP_MODEL_DIAGONALS,
	PROP_MODEL_BOUNDS = MOAIDebugLines.PROP_MODEL_BOUNDS,
	PROP_WORLD_BOUNDS = MOAIDebugLines.PROP_WORLD_BOUNDS,
	TEXT_BOX = MOAIDebugLines.TEXT_BOX,
	TEXT_BOX_BASELINES = MOAIDebugLines.TEXT_BOX_BASELINES,
	TEXT_BOX_GLYPH_BOUNDS = MOAIDebugLines.TEXT_BOX_GLYPH_BOUNDS,
	TEXT_BOX_GLYPHS = MOAIDebugLines.TEXT_BOX_GLYPHS,
	TEXT_BOX_LAYOUT = MOAIDebugLines.TEXT_BOX_LAYOUT,
	-- TOTAL_STYLES = MOAIDebugLines.TOTAL_STYLES,
}

---------------------------------------------------------------------------------
--
-- @type DebugDrawDock
--
---------------------------------------------------------------------------------

local DebugDrawDock = Class( "DebugDrawDock" )

function DebugDrawDock:init()
	--
end

---------------------------------------------------------------------------------
function DebugDrawDock:getDrawNames()
	local names = {}
	for key, _ in pairs(DEBUG_DRAW) do
		table.push( names, tostring(key) )
	end
	return tableToList(names)
end

---------------------------------------------------------------------------------
function DebugDrawDock:setDrawFlag( key, show )
	local name = DEBUG_DRAW[key]
	MOAIDebugLines.showStyle( name, show )
end

function DebugDrawDock:setDrawStyle( key, width, r, g, b, a )
	local name = DEBUG_DRAW[key]
	MOAIDebugLines.setStyle( name, width, r, g, b, a )
end

---------------------------------------------------------------------------------

debugDraw = DebugDrawDock()
