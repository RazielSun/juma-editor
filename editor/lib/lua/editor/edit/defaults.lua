--------------------------------------------------------------------------------
-- # from tommo gii
--------------------------------------------------------------------------------

addColor( 'white', 1,1,1,1 )
addColor( 'black', 0,0,0,1 )

local alpha = 0.8

addColor( 'selection', 0,1,1, alpha )
addColor( 'handle-x',  1,0,0, alpha )
addColor( 'handle-y',  0,1,0, alpha )
addColor( 'handle-z',  0,0,1, alpha )
addColor( 'handle-all', 1,1,0, alpha )
addColor( 'handle-active', 1,1,0, alpha )

addColor( 'handle-previous', 1,0,0, .3 )

addColor( 'gizmo_trigger', hexcolor( '#6695ff', 0.1 ) )
addColor( 'gizmo_trigger_border', hexcolor( '#6695ff', 0.7 ) )

addColor( 'cp',  0,1,0, alpha )
addColor( 'cp-border',  1,1,1, alpha )

addColor( 'misc',  hexcolor( '#6695ff', 0.1 ) )
addColor( 'misc-transform',  hexcolor( '#b8ff00', 1 ) )

addColor( 'camera-bound', hexcolor( '#ffc900', alpha ) )

--------------------------------------------------------------------------------
--
--------------------------------------------------------------------------------

-- MOAIDebugLines.showStyle( MOAIDebugLines.TEXT_BOX, true )
-- MOAIDebugLines.setStyle( MOAIDebugLines.TEXT_BOX, 1, 1, 1, 1, 1 )

		-- COLLISION_ACTIVE_PROP_BOUNDS,
		-- COLLISION_ACTIVE_OVERLAP_PROP_BOUNDS,
		-- COLLISION_ACTIVE_TOUCHED_PROP_BOUNDS,
		-- COLLISION_OVERLAP_PROP_BOUNDS,
		-- PARTITION_CELLS,
		-- PARTITION_PADDED_CELLS,
		-- PROP_MODEL_AXIS,
		-- PROP_MODEL_DIAGONALS,
		-- PROP_MODEL_BOUNDS,
		-- PROP_WORLD_BOUNDS,
		-- TEXT_BOX,
		-- TEXT_BOX_BASELINES,
		-- TEXT_BOX_GLYPH_BOUNDS,
		-- TEXT_BOX_GLYPHS,
		-- TEXT_BOX_LAYOUT,
		-- TOTAL_STYLES,