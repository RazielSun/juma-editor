
local Scene = require("scenes.Scene")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasScene
--
---------------------------------------------------------------------------------

local EditorCanvasScene = Class( Scene, "EditorCanvasScene" )

function EditorCanvasScene:init( option )
	local option = option or {}
	option.viewport = option.viewport or MOAIViewport.new()
	self.EDITOR_TYPE = "scene"
	Scene.init(self, option)
end

function EditorCanvasScene:getRootGroup()
    return self.rootGroup
end

function EditorCanvasScene:setRootGroup( group )
	Scene.setRootGroup( self, group )
	for _, ent in ipairs(group.children) do
		Scene.addEntity( self, ent )
	end
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

return EditorCanvasScene
