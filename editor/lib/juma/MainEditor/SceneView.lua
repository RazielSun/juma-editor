
view = false

function createScene( path )
	local scene = createEditorCanvasScene()
	if path then
		local group = EntityManager:load( path )
		if group then
			scene:setRootGroup( group )
		end
	end
	return scene
end

function saveScene( path )
	scene = getScene()
	if scene then
		return EntityManager:save( path, scene:getRootGroup() )
	end
	return false
end

function getScene()
	if view then
		return view.scene
	end
	return false
end

function viewCreated()
	return view ~= false
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

-- function GraphEditor:saveSceneAs( path )
-- 	local scene = self.scene
-- 	if scene then
-- 		return EntityManager:save( path, scene:getRootGroup() )
-- 	end
-- 	return nil
-- end

-- function GraphEditor:openScene( path )
-- 	local scene = self:getScene()
-- 	if scene then
-- 		local group = EntityManager:load( path )
-- 		if group then
-- 			scene:setRootGroup( group )
-- 		end
-- 		return scene
-- 	end
-- 	return nil
-- end

-- function GraphEditor:openSceneAs( path )
-- 	local scene = self:getScene()
-- 	if scene then
-- 		local group = EntityManager:loadByPath( path )
-- 		if group then
-- 			scene:setRootGroup( group )
-- 		end
-- 		return scene
-- 	end
-- 	return nil
-- end