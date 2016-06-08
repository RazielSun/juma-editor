
local EditorScene = require("core.EditorScene")

---------------------------------------------------------------------------------
--
-- @type BaseEditorScene
--
---------------------------------------------------------------------------------

local BaseEditorScene = Class( EditorScene, "BaseEditorScene" ):FIELDS{
	Field("bg_color"):type('color'):getset('BGColor'):label('BGColor');
}

function BaseEditorScene:init( option )
	local option = option or {}
	self.bg_color = { 0.06, 0.06, 0.06, 1.0 }
	EditorScene.init(self, option)
end

---------------------------------------------------------------------------------
function BaseEditorScene:getBGColor()
	return unpack(self.bg_color)
end

function BaseEditorScene:setBGColor( r, g, b, a )
	self.bg_color = { r, g, b, a }
	self:updateBGColor()
end

function BaseEditorScene:updateBGColor()
	local fb = self:getFrameBuffer()
	if fb then
		fb:setClearColor( unpack(self.bg_color) )
	end
end

function BaseEditorScene:getFrameBuffer( index )
	local index = index or 1
	local context = RenderContextMgr:get( self.contextName )
	if context then
		return context.bufferTable[index]
	end
	return nil
end

---------------------------------------------------------------------------------
function BaseEditorScene:setLoadedPath( path )
	local data = Loader:load( path )
	if data then
		EditorScene.setRootGroup( self, data )
		for _, ent in ipairs(data.children) do
			EditorScene.addEntity( self, ent )
		end
	end
end

function BaseEditorScene:setEnv( env )
	self.env = env
	self.contextName = env.contextName
end

function BaseEditorScene:getEnv()
	return self.env
end

function BaseEditorScene:getContextName()
	return self.contextName
end

function BaseEditorScene:getCanvasSize()
	local s = self.env.getCanvasSize()
	return s[0], s[1]
end

function BaseEditorScene:hideCursor()
	return self.env.hideCursor()
end

function BaseEditorScene:setCursor( id )
	return self.env.setCursor( id )
end

function BaseEditorScene:showCursor()
	return self.env.showCursor()
end

function BaseEditorScene:setCursorPos( x, y )
	return self.env.setCursorPos( x, y )
end

function BaseEditorScene:startUpdateTimer( fps )
	return self.env.startUpdateTimer( fps )
end

function BaseEditorScene:stopUpdateTimer()
	return self.env.stopUpdateTimer()
end

function BaseEditorScene:save( path )
	return Loader:save( path, self:getRootGroup() )
end

---------------------------------------------------------------------------------

return BaseEditorScene
