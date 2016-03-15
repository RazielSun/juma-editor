--------------------------------------------------------------------
-- Setup package path

function editorAsset( asset )
	return ASSET_EDITOR_PATH .. '/' .. asset
end

local Editor = require("core.Editor")

editor = Editor()