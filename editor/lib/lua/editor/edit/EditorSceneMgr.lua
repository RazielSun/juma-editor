local EditorScene = require("edit.EditorScene")

---------------------------------------------------------------------------------
--
-- @type EditorSceneMgr
--
---------------------------------------------------------------------------------

local EditorSceneMgr = {}

EditorSceneMgr.scenes = {}
EditorSceneMgr.currentKey = nil
EditorSceneMgr.currentScene = nil

---------------------------------------------------------------------------------

function EditorSceneMgr:addScene( scene )
	local key = scene:getContextName()
	self.scenes[key] = scene

	RenderContextMgr:pushRenderTable( key, scene.layers )

	self.currentScene = scene
	self.currentKey = key

	return scene
end

function EditorSceneMgr:getCurrentScene()
	local key = RenderContextMgr:getCurrentContextKey()
	if key == self.currentKey then
		return self.currentScene
	end

	self.currentScene = self.scenes[key]
	self.currentKey = key
	return self.currentScene
end

---------------------------------------------------------------------------------

return EditorSceneMgr