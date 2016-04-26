
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
	self.EDITOR_TYPE = "ui"

	local jui = JUI()
	jui:setSize( 320, 480 )
	self.jui = jui
	self:setHudLayers(jui._renderables)

	local screen = UIScreen( { viewport = self.viewport } )
	jui:openScreenInternal( screen ) -- THIS IS FOR CONTENT

	local secondScreen = UIScreen( { viewport = self.viewport } )
	jui:openScreenInternal( secondScreen ) -- THIS IS FOR CANVAS VIEW LAYER ITEMS
end

function EditorCanvasUIScene:getRootGroup()
	return self.jui:getScreen(2)
end

function EditorCanvasUIScene:setLoadedPath( path )
	local data = Loader:load( path )
	if data then
		local children = table.dup(data.children)
		data:removeChildren()
		local topScreen = self.jui:getScreen(2)
		topScreen:removeChildren()
		topScreen:setChildren(children)
	end
end

---------------------------------------------------------------------------------

return EditorCanvasUIScene
