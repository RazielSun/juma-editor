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

AssetsGrabber = require("edit.AssetsGrabber") --# FIXME

require("edit.EditorCanvas.SceneView")

function refreshAssets()
	AssetsGrabber.grabFromResourceMgr()
end