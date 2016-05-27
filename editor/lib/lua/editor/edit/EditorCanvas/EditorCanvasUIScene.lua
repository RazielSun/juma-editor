
local EditorCanvasScene = require("edit.EditorCanvas.EditorCanvasScene")
local JUI = require("ui.JUI")
local UIScreen = require("ui.UIScreen")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasUIScene
--
---------------------------------------------------------------------------------

local EditorCanvasUIScene = Class( EditorCanvasScene, "EditorCanvasUIScene" ):FIELDS{
}

function EditorCanvasUIScene:init( option )
	local option = option or {}
	EditorCanvasScene.init(self, option)

	local jui = JUI()
	jui:setSize( 320, 480 )
	self.jui = jui

	local renderTbl = self:getRender()
	table.insert( renderTbl, jui._renderables )

	local screen = UIScreen( { viewport = self.viewport } )
	jui:openScreenInternal( screen )
end

function EditorCanvasUIScene:getRootGroup()
	return self.jui:getScreen(1)
end

function EditorCanvasUIScene:setLoadedPath( path )
	local data = Loader:load( path )
	if data then
		local children = table.dup(data.children)
		data:removeChildren()
		local topScreen = self.jui:getScreen(1)
		topScreen:removeChildren()
		topScreen:setChildren(children)
	end
end

---------------------------------------------------------------------------------

return EditorCanvasUIScene
