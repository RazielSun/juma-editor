--------------------------------------------------------------------
--Setup package path
--------------------------------------------------------------------
package.path = package.path
	.. ( ';' .. LIB_EDITOR_PATH .. '/?.lua' )

MOAIApp = MOAIApp or require ('MOAIApp')
MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')

require("KeyMap")

RenderContext = require("RenderContext")
Bridge = require("Bridge")
Editor = require("Editor")

--------------------------------------------------------------------
local function onContextChange( ctx, oldCtx )
	Editor.setCurrentRenderContext( ctx )
end

RenderContext.addContextChangeListeners( onContextChange )

function getEditorAssetPath( asset )
	return ASSETS_EDITOR_PATH .. '/' .. asset
end