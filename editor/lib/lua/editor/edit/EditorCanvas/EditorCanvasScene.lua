
local EditorScene = require("edit.EditorScene")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasScene
--
---------------------------------------------------------------------------------

local EditorCanvasScene = Class( EditorScene, "EditorCanvasScene" ):FIELDS{
	Field("bg_color"):type('color'):getset('BGColor'):label('BGColor');
}

function EditorCanvasScene:init( option )
	local option = option or {}
	option.viewport = option.viewport or MOAIViewport.new()
	self.EDITOR_TYPE = "scene"
	self.bg_color = { 0.06, 0.06, 0.06, 1.0 }
	EditorScene.init(self, option)
end

---------------------------------------------------------------------------------
function EditorCanvasScene:getBGColor()
	return self.bg_color
end

function EditorCanvasScene:setBGColor( r, g, b, a )
	self.bg_color = { r, g, b, a }
	self:updateBGColor()
end

function EditorCanvasScene:updateBGColor()
	local fb = self:getFrameBuffer()
	if fb then
		fb:setClearColor( unpack(self.bg_color) )
	end
end

function EditorCanvasScene:getFrameBuffer( index )
	local index = index or 1
	local context = RenderContextMgr:get( self.contextName )
	if context then
		return context.bufferTable[index]
	end
	return nil
end

---------------------------------------------------------------------------------
function EditorCanvasScene:setLoadedPath( path )
	local data = Loader:load( path )
	if data then
		EditorScene.setRootGroup( self, data )
		for _, ent in ipairs(data.children) do
			EditorScene.addEntity( self, ent )
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
