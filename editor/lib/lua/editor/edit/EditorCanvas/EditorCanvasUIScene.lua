
local EditorCanvasScene = require("edit.EditorCanvas.EditorCanvasScene")
local JUI = require("ui.JUI")
local UIScreen = require("ui.UIScreen")

---------------------------------------------------------------------------------
--
-- @type EditorCanvasUIScene
--
---------------------------------------------------------------------------------

local EditorCanvasUIScene = Class( EditorCanvasScene, "EditorCanvasUIScene" )

function EditorCanvasUIScene:init( option )
	local option = option or {}
	EditorCanvasScene.init(self, option)
	self.EDITOR_TYPE = "ui"

	local jui = JUI()
	jui:setSize( 320, 480 )
	self.jui = jui
	self:setHudLayers(jui._renderables)

	local screen = UIScreen( { viewport = self.viewport } )
	jui:openScreenInternal( screen )
end

function EditorCanvasUIScene:getRootGroup()
	return self.jui._activeScreens[1]
end

function EditorCanvasUIScene:setRootGroup( group )
	local children = table.dup(group.children)
	group:removeChildren()
	local topScreen = self.jui._activeScreens[1]
	topScreen:removeChildren()
	topScreen:setChildren(children)
end

---------------------------------------------------------------------------------

return EditorCanvasUIScene
