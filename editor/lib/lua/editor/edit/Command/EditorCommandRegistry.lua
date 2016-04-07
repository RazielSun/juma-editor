
---------------------------------------------------------------------------------
--
-- @type EditorCommandRegistry
--
---------------------------------------------------------------------------------

local registerCommandClasses = {}

function getEditorCommandRegistry( fullname )
	return registerCommandClasses[fullname]
end

function editorCommandRegistryClass( clazz, fullname )
	registerCommandClasses[fullname] = clazz
	registerLuaEditorCommand( fullname )
end