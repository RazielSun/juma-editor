--------------------------------------------------------------------------------
-- Assets from data
--------------------------------------------------------------------------------

function projEditorAsset( asset )
	if PROJECT_EDITOR_ASSETS_PATH then
		return PROJECT_EDITOR_ASSETS_PATH .. '/' .. asset
	end
	return nil
end

function editorAssetPath( asset )
	if EDITOR_ASSETS_PATH then
		return EDITOR_ASSETS_PATH .. '/' .. asset
	end
	return nil
end

--------------------------------------------------------------------------------
-- Assets Grabber
--
AssetsGrabber = require("assets.AssetsGrabber")

function refreshAssets()
	AssetsGrabber.grabFromResourceMgr()
end

refreshAssets()