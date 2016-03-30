local Scene = require("scenes.Scene")
local InputDevice = require("input.InputDevice")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasScene
--
---------------------------------------------------------------------------------

local EditorCanvasScene = Class( Scene, "EditorCanvasScene" )

function EditorCanvasScene:init( option )
	Scene.init(self, option)
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

function EditorCanvasScene:getCanvasSize()
	local s = self.env.getCanvasSize()
	return s[0], s[1]
end

function EditorCanvasScene:hideCursor()
	return self.env.hideCursor()
end

function EditorCanvasScene:setCursor( id )
	return self.env.setCursor( id )
end

function EditorCanvasScene:showCursor()
	return self.env.showCursor()
end

function EditorCanvasScene:setCursorPos( x, y )
	return self.env.setCursorPos( x, y )
end

function EditorCanvasScene:startUpdateTimer( fps )
	return self.env.startUpdateTimer( fps )
end

function EditorCanvasScene:stopUpdateTimer()
	return self.env.stopUpdateTimer()
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

	env._delegate:updateHooks()
	return inputDevice
end

---------------------------------------------------------------------
function createEditorCanvasScene()
	local env = getfenv( 2 )
	local scene = EditorCanvasScene( { viewport = MOAIViewport.new() } )
	scene:setEnv( env )

	-- FIXME
	-- function env.onResize( w, h )
	-- 	scene:resize( w, h )
	-- 	-- scene.cameraCom:setScreenSize( w, h )
	-- end

	function env.onLoad()
	end

	local inputDevice = createEditorCanvasInputDevice( env )

	scene.inputDevice = inputDevice

	-- function env.EditorInputScript()
	-- 	return mock.InputScript{ device = inputDevice }
	-- end

	return scene
end 
