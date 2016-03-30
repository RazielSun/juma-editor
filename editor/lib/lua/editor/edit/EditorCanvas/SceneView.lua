
local CanvasView = require("edit.CanvasView.CanvasView")

---------------------------------------------------------------------------------
--
-- @type SceneView
--
---------------------------------------------------------------------------------

function createSceneView( scene, env )
	local view = CanvasView( env )
	view.EDITOR_TYPE = scene.EDITOR_TYPE
	return view
end