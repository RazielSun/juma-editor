
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
-- @type Scene and Canvas
--
---------------------------------------------------------------------------------

local sceneCanvasRegister = {}

function registerEditorSceneCanvasForType( scene, canvas, typ )
	local obj = { scene = scene, canvas = canvas }
	sceneCanvasRegister[typ] = obj
end

function getEditorSceneForType( typ )
	local obj = sceneCanvasRegister[typ]
	if not obj then
		print("No Scene for type:", typ)
	end
	local builder = require(obj.scene)
	return builder
end

function getEditorCanvasForType( typ )
	local obj = sceneCanvasRegister[typ]
	if not obj then
		print("No Scene for type:", typ)
	end
	local builder = require(obj.canvas)
	return builder
end
