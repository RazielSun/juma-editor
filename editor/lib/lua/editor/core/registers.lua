
---------------------------------------------------------------------------------
--
-- @type Class Register
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

---------------------------------------------------------------------------------
--
-- @type SceneView
--
---------------------------------------------------------------------------------

local sceneViewRegister = {}

function registerCanvasViewFor( clazz, stype )
	sceneViewRegister[stype] = clazz
end

function getCanvasViewFor( stype )
	return sceneViewRegister[stype]
end

---------------------------------------------------------------------------------
--
-- @type builders
--
---------------------------------------------------------------------------------

local editorCanvasRegistry = {}

function setEditorCanvasSceneForType( clazz, stype )
	editorCanvasRegistry[stype] = clazz
end

function getEditorCanvasScene( stype )
	if not editorCanvasRegistry[stype] then
		print("ERROR! Not find", stype, "EditorCanvasScene")
		return nil
	end
	return editorCanvasRegistry[stype]
end