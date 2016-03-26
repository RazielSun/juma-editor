require("edit.common")
require("edit.defaults")
require("edit.helpers")

--------------------------------------------------------------------------------
-- Setups

RenderContextMgr = require("edit.RenderContextMgr")
EditorSceneMgr = require("edit.EditorSceneMgr")

require("edit.EditorCanvasScene")
require("edit.tools.CanvasToolManager")
require("edit.tools.TransformTools")
require("edit.tools.DragCameraTool")
require("edit.tools.TargetTool")

--# FIXME
AssetsGrabber = require("edit.AssetsGrabber")

function refreshAssets()
	AssetsGrabber.grabFromResourceMgr()
end