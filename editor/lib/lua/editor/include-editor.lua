require("edit.common")
require("edit.registers")
require("edit.defaults")
require("edit.helpers")

--------------------------------------------------------------------------------
-- Setups

RenderContextMgr = require("edit.RenderContextMgr")

require("edit.EditorCanvas.common")
require("edit.CanvasView.CanvasToolManager")
require("edit.tools.common")
require("edit.Command.EditorCommandRegistry")

--------------------------------------------------------------------------------
-- Assets Grabber
--
AssetsGrabber = require("edit.AssetsGrabber")

function refreshAssets()
	AssetsGrabber.grabFromResourceMgr()
end

refreshAssets()