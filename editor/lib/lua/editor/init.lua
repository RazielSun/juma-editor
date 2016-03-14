--------------------------------------------------------------------
-- Setup package path

package.path = package.path
	.. ( ';' .. LIB_FRAMEWORK_PATH .. '/?.lua' )
	.. ( ';' .. LIB_EDITOR_PATH .. '/?.lua' )

function editorAsset( asset )
	return ASSET_EDITOR_PATH .. '/' .. asset
end

--------------------------------------------------------------------
-- Init Lua Framework

require("include")

assert(Class, "No 'Class' constructor for Editor Lua Framework")

--------------------------------------------------------------------
-- Init Editor Framework
require("util.bridge")
require("util.keymap")

MOAIApp = MOAIApp or require ('MOAIApp')
MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')

local Editor = require("core.Editor")

editor = Editor()