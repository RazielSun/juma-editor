local EditorScene = require("edit.EditorScene")
local InputDevice = require("core.InputDevice")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasScene
--
---------------------------------------------------------------------------------

local EditorCanvasScene = Class( EditorScene, "EditorCanvasScene" )

function EditorCanvasScene:init( params )
	EditorScene.init(self, params)
end

function EditorCanvasScene:setEnv( env )
	self.env = env
	self.contextName = env.contextName
end

function EditorCanvasScene:getEnv()
	return self.env
end

function EditorCanvasScene:getContextName()
	return self.contextName
end

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

	-- env._delegate:updateHooks()
	return inputDevice
end

---------------------------------------------------------------------
function createEditorCanvasScene()
	local env = getfenv( 2 )
	local scene = EditorCanvasScene()
	scene:setEnv( env )

	EditorSceneMgr:addScene( scene )

	function env.onResize( w, h )
		scene:resize( w, h )
		-- scene.cameraCom:setScreenSize( w, h )
	end

	function env.onLoad()
	end

	local inputDevice = createEditorCanvasInputDevice( env )

	-- function env.EditorInputScript()
	-- 	return mock.InputScript{ device = inputDevice }
	-- end

	scene:setInputDevice( inputDevice )
	return scene
end 
