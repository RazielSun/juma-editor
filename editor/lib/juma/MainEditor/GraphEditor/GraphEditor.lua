local Entity = require("core.Entity")

local GraphEditor = Class("GraphEditor")

function GraphEditor:init()
	-- print("GraphEditor inited")
end

function GraphEditor:getScene()
	return EditorLayoutMgr:getCurrentScene()
end

function GraphEditor:getSceneRootNode()
	local scene = EditorLayoutMgr:getCurrentScene()
	return scene:getRootNode()
end

function GraphEditor:createEntity()
	local node = Entity()
	local scene = self:getScene()
	scene:addNodeToActiveGroup( node )
	return node
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

graphEditor = GraphEditor()