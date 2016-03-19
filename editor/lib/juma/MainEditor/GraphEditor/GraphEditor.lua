local Entity = require("core.Entity")

local GraphEditor = Class("GraphEditor")

function GraphEditor:init()
	self.items = {}
end

function GraphEditor:getScene()
	return EditorSceneMgr:getScene()
end

function GraphEditor:createEntity()
	local entity = Entity()
	table.push( self.items, entity )
	return entity
end

graphMgr = GraphEditor()