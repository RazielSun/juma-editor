local Sprite = require("ui.Sprite")
local Label = require("ui.Label")
local Button = require("ui.Button")
local Group = require("ui.Group")

---------------------------------------------------------------------------------
--
-- @type GraphEditor
--
---------------------------------------------------------------------------------

local GraphEditor = Class("GraphEditor")

---------------------------------------------------------------------------------
function GraphEditor:init()
	-- print("GraphEditor inited")
end

---------------------------------------------------------------------------------
function GraphEditor:getScene()
	return EditorLayoutMgr:getCurrentScene()
end

function GraphEditor:getSceneRootNode()
	local scene = EditorLayoutMgr:getCurrentScene()
	return scene:getRootNode()
end

function GraphEditor:createWidget( widget_type )
	local widget = nil
	if widget_type == "Sprite" then
		widget = Sprite()
	elseif widget_type == "Label" then
		widget = Label()
	elseif widget_type == "Button" then
		widget = Button()
	elseif widget_type == "Group" then
		widget = Group()
	end

	if widget then
		local scene = self:getScene()
		scene:addWidgetToActiveGroup( widget )
	end
	return widget
end

function GraphEditor:removeWidget( widget )
	local success = false

	if widget then
		local scene = self:getScene()
		success = scene:removeWidgetToActiveGroup( widget )
	end

	return success
end

function GraphEditor:saveScene()
	local scene = self:getScene()
	if scene then
		return scene:save()
	end
	return nil
end

function GraphEditor:loadScene( path )
	local scene = self:getScene()
	if scene then
		scene:load( path )
		return scene.rootNode
	end
	return nil
end

---------------------------------------------------------------------------------

graphEditor = GraphEditor()