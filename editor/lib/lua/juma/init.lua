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
-- Init Editor Framework
require("bridge")
require("keymap")

MOAIApp = MOAIApp or require('MOAIApp')
MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')


require("setup_editor")