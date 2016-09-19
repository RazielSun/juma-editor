
local InputDevice = require("input.InputDevice")

---------------------------------------------------------------------------------
--
-- @type create methods
--
---------------------------------------------------------------------------------

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

	local builder = getEditorSceneForType( stype )
	local scene = nil

	if builder then
		scene = builder()
		scene.EDITOR_TYPE = stype
		if not scene.SCENE_TYPE then
			scene.SCENE_TYPE = stype
		end
		scene:setEnv( env )
		scene:setInputDevice( createEditorCanvasInputDevice( env ) )
	end

	return scene
end

---------------------------------------------------------------------
function createSceneView( scene, env )
	local stype = scene.EDITOR_TYPE or 'scene'
	local builder = getEditorCanvasForType( stype )
	local view = builder( env )
	view.EDITOR_TYPE = stype
	return view
end