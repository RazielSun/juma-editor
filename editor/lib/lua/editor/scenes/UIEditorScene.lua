
local BaseEditorScene = require("scenes.BaseEditorScene")

local JUI = require("ui.JUI")
local UIScreen = require("ui.UIScreen")

---------------------------------------------------------------------------------
--
-- @type UIEditorScene
--
---------------------------------------------------------------------------------

local UIEditorScene = Class( BaseEditorScene, "UIEditorScene" ):FIELDS{
}

function UIEditorScene:init( option )
	local option = option or {}
	BaseEditorScene.init(self, option)

	self.SCENE_TYPE = "ui"

	local viewport = MOAIViewport.new()
	self.viewport = viewport

	local jui = JUI()
	jui:setSize( 320, 480 )
	self.jui = jui

	local renderTbl = self:getRender()
	table.insert( renderTbl, jui._renderables )

	local screen = UIScreen( { viewport = viewport } )
	self.jui:openScreenInternal( screen )
end

function UIEditorScene:getRootGroup()
	return self.jui:getScreen(1)
end

function UIEditorScene:setLoadedPath( path )
	local data = Loader:load( path )

	if data then
		local children = table.dup(data.children)
		data:removeChildren()

		local screen = self:getRootGroup()
		screen:removeChildren()
		screen:setChildren(children)
	end
end

---------------------------------------------------------------------------------

return UIEditorScene
