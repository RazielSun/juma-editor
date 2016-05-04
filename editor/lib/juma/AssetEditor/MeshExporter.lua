
view = false

function onLoad()
	local stype = '3d'
	local scene = createEditorCanvasScene( stype )
	scene.EDITOR_TYPE = stype

	onSceneOpen( scene )
end

-- function saveScene( path )
-- 	scene = getScene()
-- 	if scene then return scene:save( path ) end
-- 	return false
-- end

-- function getScene()
-- 	if view then return view.scene end
-- 	return false
-- end

-- function viewCreated()
-- 	return view ~= false
-- end

function onSceneOpen( scene )
	local key = RenderContextMgr:getCurrentContextKey()
	RenderContextMgr:pushRenderTable( key, scene.renderTbl )

	scene.contextName = key
	scene:updateBGColor()

	local env = getfenv()
	view = createSceneView( scene, env )

	scene:addEntity( view )
	scene.canvasView = view
end

function onSceneClose()
	view = false
end

function onResize( w, h )
	if view then
		view:resizeCanvas( w, h )
	end
end
