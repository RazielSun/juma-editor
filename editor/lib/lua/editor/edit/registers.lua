
---------------------------------------------------------------------------------
--
-- @type
--
---------------------------------------------------------------------------------

local registerClassTypes = {}
local _mt = {__mode = "k"}

function getEditorRegistry( etype )
	return tableToDict(registerClassTypes[etype])
end

function editorRegistryClassType( clazz, etype )
	local map = registerClassTypes[etype]
	if not map then
		registerClassTypes[etype] = setmetatable({}, _mt)
		map = registerClassTypes[etype]
	end

	table.insert( map, clazz )
end