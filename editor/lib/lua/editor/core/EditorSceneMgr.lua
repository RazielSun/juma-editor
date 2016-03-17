local Entity = require("core.Entity")
local EntityGroup = require("core.EntityGroup")

local EditorSceneMgr = {}

EditorSceneMgr.scenes = {}
EditorSceneMgr.currentKey = nil
EditorSceneMgr.currentScene = nil

function EditorSceneMgr:setupScene()
	local key = RenderContextMgr:getCurrentContextKey()

	local scene = self.scenes[key]
	if not scene then
		scene = self:newScene()
		self.scenes[key] = scene
	end

	RenderContextMgr:pushRenderTable( key, { scene.layer } )

	self.currentScene = scene
	self.currentKey = key

	return scene
end

function EditorSceneMgr:getScene()
	local key = RenderContextMgr:getCurrentContextKey()
	if key == self.currentKey then
		return self.currentScene
	end

	self.currentScene = self.scenes[key]
	self.currentKey = key
	return self.currentScene
end

--------------------------------------------------------------------
--
local EditCanvasContext = {}

function EditorSceneMgr:newScene()
	local layer = MOAILayer.new()
	local camera = MOAICamera2D.new()
	local viewport = MOAIViewport.new()

	layer:setViewport(viewport)
	layer:setCamera(camera)

	local group = EntityGroup()
	group:setLayer( layer )

	local scene = {
		layer      	= layer,
		root		= group,
		camera     	= camera,
		cameraScl  	= 1,
		viewport   	= viewport,
		viewWidth  	= 0,
		viewHeight 	= 0,
	}
	scene = setmetatable( scene, { __index = EditCanvasContext } )

	return scene
end

function EditCanvasContext:resize( w, h )
	self.viewport:setSize(w,h)
	self.viewport:setScale(w,h)

	self.viewWidth, self.viewHeight = w, h
end

return EditorSceneMgr