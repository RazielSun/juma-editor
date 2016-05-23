
local defaultSortMode = MOAILayer.SORT_PRIORITY_DESCENDING --SORT_Z_ASCENDING

---------------------------------------------------------------------------------
--
-- @type PickingManager
--
---------------------------------------------------------------------------------

local PickingManager = Class( "PickingManager" )

function PickingManager:init( option )
	option = option or {}
	self:setTargetScene( option.scene )
end

function PickingManager:setTargetScene( scene )
	self.targetScene = scene
end

---------------------------------------------------------------------------------
function PickingManager:pickPoint( x, y, pad )
	for i, layer in ipairs( self:getVisibleLayers() ) do
		local partition = layer:getPartition()
		local result = { partition:propListForPoint( x, y, 0, defaultSortMode ) } --propListForRay  -1000, 0, 0, 1,
		for i, prop in ipairs( result ) do
			local widget = prop.widget
			local com = prop.component
			if widget and not widget.FLAG_EDITOR_OBJECT then
				return { widget }
			elseif com and not com.FLAG_EDITOR_OBJECT then
				return { com.entity }
			end
		end
	end
	return {}
end

function PickingManager:pickRect( x0, y0, x1, y1, pad )
	local picked = {}
	for i, layer in ipairs( self:getVisibleLayers() ) do
		local partition = layer:getPartition()
		local result = { partition:propListForRect( x0, y0, x1, y1, defaultSortMode ) }
		for i, prop in ipairs( result ) do
			local widget = prop.widget
			local com = prop.component
			if widget and not widget.FLAG_EDITOR_OBJECT then
				picked[ widget ] = true
			elseif com and not com.FLAG_EDITOR_OBJECT then
				picked[ com.entity ] = true
			end
		end
	end

	return table.keys(picked)
end

function PickingManager:getVisibleLayers()
	local layers = {}
	self:collectLayers( self.targetScene:getRender(), layers )
	return table.reverse( layers )
end

function PickingManager:collectLayers( source, layers )
	for i, layer in ipairs( source ) do
		if type(layer) == 'table' then
			self:collectLayers( layer, layers )
		else
			table.insert( layers, layer )
		end
	end
	return layers
end
---------------------------------------------------------------------------------

return PickingManager
