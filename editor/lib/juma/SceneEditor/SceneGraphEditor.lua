local Entity = require("core.Entity")

local SceneGraphEditor = Class("SceneGraphEditor")

function SceneGraphEditor:init()
	self.items = {}
end

function SceneGraphEditor:getScene()
	return EditorSceneMgr:getScene()
end

function SceneGraphEditor:createEntity()
	local entity = Entity()
	table.push( self.items, entity )
	return entity
end

graphMgr = SceneGraphEditor()