--------------------------------------------------------------------
-- Setup package path

function editorAsset( asset )
	return ASSET_EDITOR_PATH .. '/' .. asset
end

function setGameResolution( width, height )
	MOAIEnvironment.setValue('horizontalResolution', width)
	MOAIEnvironment.setValue('verticalResolution', height)
end

--------------------------------------------------------------------
-- Setups

Editor = require("core.Editor")
RenderContextMgr = require("core.RenderContextMgr")
EditorSceneMgr = require("core.EditorSceneMgr")

--------------------------------------------------------------------------------
-- Resources

if ResourceMgr then
	ResourceMgr:addResourceDirectory( ASSET_EDITOR_PATH )
end