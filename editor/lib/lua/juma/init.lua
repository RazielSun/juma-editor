--------------------------------------------------------------------
-- Setup package path

package.path = package.path
	.. ( ';' .. LIB_FRAMEWORK_LUA_PATH .. '/?.lua' )
	.. ( ';' .. LIB_EDITOR_LUA_PATH .. '/?.lua' )
	.. ( ';' .. LIB_JUMA_LUA_PATH .. '/?.lua' )

--------------------------------------------------------------------
-- Init Lua Framework
require("include")
assert(Class, "No 'Class' constructor for Editor Lua Framework")

--------------------------------------------------------------------
-- Init Juma
require("keymap")
require("bridge")
require("ModelProvider")
require("MOAIModelProvider")

MOAIApp = MOAIApp or require('MOAIApp')
MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')

--------------------------------------------------------------------
-- Init Editor Framework
require("setup_editor")