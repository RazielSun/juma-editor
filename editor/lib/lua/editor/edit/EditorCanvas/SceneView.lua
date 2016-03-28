
local CanvasView = require("edit.CanvasView.CanvasView")

---------------------------------------------------------------------------------
--
-- @type SceneView
--
---------------------------------------------------------------------------------

function createSceneView( scene, env )
	local view = CanvasView( env )
	return view
end