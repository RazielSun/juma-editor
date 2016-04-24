
local Scene = require("scenes.Scene")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasScene
--
---------------------------------------------------------------------------------

local EditorCanvasScene = Class( Scene, "EditorCanvasScene" ):FIELDS{
	Field("bg_color"):type('color'):getset('BGColor'):label('BGColor');
}

function EditorCanvasScene:init( option )
	local option = option or {}
	option.viewport = option.viewport or MOAIViewport.new()
	self.EDITOR_TYPE = "scene"
	self.bg_color = { 0.06, 0.06, 0.06, 1.0 }
	Scene.init(self, option)
end

function EditorCanvasScene:setLoadedPath( path )
	local data = Loader:load( path )
	if data then
		Scene.setRootGroup( self, data )
		for _, ent in ipairs(data.children) do
			Scene.addEntity( self, ent )
		end
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

function EditorCanvasScene:save( path )
	return Loader:save( path, self:getRootGroup() )
end

---------------------------------------------------------------------------------

return EditorCanvasScene
