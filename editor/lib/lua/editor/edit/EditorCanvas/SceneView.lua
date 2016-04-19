
---------------------------------------------------------------------------------
--
registerAssetNodeInLibrary( "scene", "create_scene" )
registerAssetNodeInLibrary( "ui", "create_scene" )

---------------------------------------------------------------------------------
--

local CanvasView = require("edit.CanvasView.CanvasView")

---------------------------------------------------------------------------------
--
-- @type SceneView
--
---------------------------------------------------------------------------------

local sceneViewRegister = {}

function registerCanvasViewFor( clazz, stype )
	sceneViewRegister[stype] = clazz
end

function createSceneView( scene, env )
	local stype = scene.EDITOR_TYPE or 'scene'
	local builder = sceneViewRegister[stype]
	if not builder then
		builder = CanvasView
	end

	local view = builder( env )
	view.EDITOR_TYPE = stype
	
	return view
end

