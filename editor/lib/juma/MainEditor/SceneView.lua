
view = false

function createScene( path, stype )
	local scene = createEditorCanvasScene( stype )
	if path then scene:setLoadedPath( path ) end
	return scene
end

function saveScene( path )
	scene = getScene()
	if scene then return scene:save( path ) end
	return false
end

function getScene()
	if view then return view.scene end
	return false
end

function viewCreated()
	return view ~= false
end

function onSceneOpen( scene )
	local key = RenderContextMgr:getCurrentContextKey()
	scene.contextName = key
	RenderContextMgr:pushRenderTable( key, scene.renderTbl )

	local context = RenderContextMgr:getCurrentContext()
	local fb = context.bufferTable[1]
	fb:setClearColor( unpack(scene.bg_color) )

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
