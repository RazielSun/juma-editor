local Entity = require("core.Entity")

local SceneGraphEditor = Class("SceneGraphEditor")

function SceneGraphEditor:init()
	self.counts = 0
end

function SceneGraphEditor:getScene()
	return EditorSceneMgr:getScene()
end

function SceneGraphEditor:createEntity()
	self.counts = self.counts + 1
	local entity = Entity()
	entity.name = string.format("entity %d", self.counts)
	return entity
end

graphMgr = SceneGraphEditor()