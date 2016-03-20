local EditorScene = require("edit.EditorScene")

---------------------------------------------------------------------------------
--
-- @type EditorLayoutMgr
--
---------------------------------------------------------------------------------

local EditorLayoutMgr = {}

EditorLayoutMgr.scenes = {}
EditorLayoutMgr.currentKey = nil
EditorLayoutMgr.currentScene = nil

---------------------------------------------------------------------------------

function EditorLayoutMgr:setupScene()
	local key = RenderContextMgr:getCurrentContextKey()

	local scene = self.scenes[key]
	if not scene then
		scene = EditorScene()
		self.scenes[key] = scene
	end

	RenderContextMgr:pushRenderTable( key, { scene.layer } )

	self.currentScene = scene
	self.currentKey = key

	return scene
end

function EditorLayoutMgr:getCurrentScene()
	local key = RenderContextMgr:getCurrentContextKey()
	if key == self.currentKey then
		return self.currentScene
	end

	self.currentScene = self.scenes[key]
	self.currentKey = key
	return self.currentScene
end

---------------------------------------------------------------------------------

return EditorLayoutMgr