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

RenderContextMgr = require("edit.RenderContextMgr")
EditorLayoutMgr = require("edit.EditorLayoutMgr")

--------------------------------------------------------------------------------
-- Resources

if ResourceMgr then
	ResourceMgr:addResourceDirectory( ASSET_EDITOR_PATH )
end