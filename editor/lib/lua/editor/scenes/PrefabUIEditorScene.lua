
local UIEditorScene = require("scenes.UIEditorScene")

---------------------------------------------------------------------------------
--
-- @type PrefabUIEditorScene
--
---------------------------------------------------------------------------------

local PrefabUIEditorScene = Class( UIEditorScene, "PrefabUIEditorScene" ):FIELDS{
}

function PrefabUIEditorScene:setLoadedPath( path )
	local prefab = Loader:load( path )

	if prefab then
		local screen = self:getRootGroup()
		screen:removeChildren()
		screen:addChild(prefab)
	end
end

---------------------------------------------------------------------------------
function PrefabUIEditorScene:getPrefab()
	local screen = self:getRootGroup()
	local children = screen.children
	return children[1]
end

function PrefabUIEditorScene:save( path )
	return Loader:save( path, self:getPrefab() )
end

---------------------------------------------------------------------------------

return PrefabUIEditorScene
