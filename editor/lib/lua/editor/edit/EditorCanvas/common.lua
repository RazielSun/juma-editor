
require("edit.EditorCanvas.SceneView")

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

---------------------------------------------------------------------------------
--
-- @type create methods
--
---------------------------------------------------------------------------------
local InputDevice = require("input.InputDevice")

function createEditorCanvasInputDevice( env )
	local env = env or getfenv(2)
	local inputDevice = InputDevice( assert(env.contextName), env )

	function env.onMouseDown( btn, x, y )
		inputDevice:sendMouseEvent( 'down', x, y, btn )
	end

	function env.onMouseUp( btn, x, y )
		inputDevice:sendMouseEvent( 'up', x, y, btn )
	end

	function env.onMouseMove( x, y )
		inputDevice:sendMouseEvent( 'move', x, y, false )
	end

	function env.onMouseScroll( dx, dy, x, y )
		inputDevice:sendMouseEvent( 'scroll', dx, dy, false )
	end

	function env.onMouseEnter()
		inputDevice:sendMouseEvent( 'enter' )
	end

	function env.onMouseLeave()
		inputDevice:sendMouseEvent( 'leave' )
	end

	function env.onKeyDown( key )
		inputDevice:sendKeyEvent( key, true )
	end

	function env.onKeyUp( key )
		inputDevice:sendKeyEvent( key, false )
	end

	env._delegate:updateHooks()
	return inputDevice
end

---------------------------------------------------------------------
function createEditorCanvasScene( stype )
	stype = stype or "scene"
	local env = getfenv( 2 )

	function env.onLoad()
	end

	local builder = getEditorCanvasScene( stype )
	local scene = nil

	if builder then
		scene = builder()
		scene:setEnv( env )
		scene:setInputDevice( createEditorCanvasInputDevice( env ) )
	end

	return scene
end 

---------------------------------------------------------------------------------
local EditorCanvasScene = require("edit.EditorCanvas.EditorCanvasScene")
local EditorCanvasUIScene = require("edit.EditorCanvas.EditorCanvasUIScene")

setEditorCanvasSceneForType( EditorCanvasScene, "scene" )
setEditorCanvasSceneForType( EditorCanvasUIScene, "ui" )
setEditorCanvasSceneForType( EditorCanvasScene, "3d" )

local Canvas3DView = require("edit.CanvasView.3D.Canvas3DView")

registerCanvasViewFor( Canvas3DView, "3d" )
