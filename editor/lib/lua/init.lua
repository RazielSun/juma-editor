--------------------------------------------------------------------
--Setup package path
--------------------------------------------------------------------
package.path = package.path
	.. ( ';' .. LIB_LUA_PATH .. '/?.lua' )
	.. ( ';' .. LIB_EDITOR_PATH .. '/?.lua' )

require("Editor")