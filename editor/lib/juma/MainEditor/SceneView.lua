
view = false

function createScene()
	local scene = createEditorCanvasScene()
	return scene
end

function onSceneOpen( scene )
	local env = getfenv()
	view = createSceneView( scene, env )

	local key = RenderContextMgr:getCurrentContextKey()
	scene.contextName = key

	RenderContextMgr:pushRenderTable( key, scene.layers )

	scene:addEntity( view )
end

function onSceneClose()
	view = false
end

function onResize( w, h )
	if view then
		view:resizeCanvas( w, h )
	end
end