--------------------------------------------------------------------
-- Setup package path

package.path = package.path
	.. ( ';' .. LIB_FRAMEWORK_PATH .. '/?.lua' )
	.. ( ';' .. LIB_EDITOR_PATH .. '/?.lua' )

--------------------------------------------------------------------
-- Init Lua Framework

require("include")

--------------------------------------------------------------------
-- Init Editor Framework

MOAIApp = MOAIApp or require ('MOAIApp')
MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')

require("KeyMap")

RenderContext = require("RenderContext")
Bridge = require("Bridge")
Editor = require("Editor")

--------------------------------------------------------------------
--
local function onContextChange( ctx, oldCtx )
	Editor.setCurrentRenderContext( ctx )
end

RenderContext.addContextChangeListeners( onContextChange )

function getEditorAssetPath( asset )
	return ASSET_EDITOR_PATH .. '/' .. asset
end