--------------------------------------------------------------------
--Setup package path
--------------------------------------------------------------------
package.path = package.path
	.. ( ';' .. LIB_LUA_PATH .. '/?.lua' )

editor = require("editor.Editor")