local Entity = require("core.Entity")

local GraphEditor = Class("GraphEditor")

function GraphEditor:init()
	self.items = {}
end

function GraphEditor:getScene()
	return EditorLayoutMgr:getCurrentScene()
end

function GraphEditor:getSceneRootNode()
	local scene = EditorLayoutMgr:getCurrentScene()
	return scene:getRootNode()
end

function GraphEditor:createEntity()
	local entity = Entity()
	table.push( self.items, entity )
	return entity
end

graphEditor = GraphEditor()