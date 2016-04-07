require("edit.common")
require("edit.registers")
require("edit.defaults")
require("edit.helpers")

--------------------------------------------------------------------------------
-- Setups

RenderContextMgr = require("edit.RenderContextMgr")

require("edit.EditorCanvasScene")
require("edit.CanvasView.CanvasToolManager")
require("edit.tools.common")
require("edit.Command.EditorCommandRegistry")

AssetsGrabber = require("edit.AssetsGrabber")

require("edit.EditorCanvas.SceneView")

function refreshAssets()
	AssetsGrabber.grabFromResourceMgr()
end