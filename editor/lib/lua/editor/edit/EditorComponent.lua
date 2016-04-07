
local Component = require("entity.Component")

---------------------------------------------------------------------------------
--
-- @type EditorComponent
--
---------------------------------------------------------------------------------

local EditorComponent = Class( Component, "EditorComponent" )


function EditorComponent:init( option )
	self.FLAG_EDITOR_OBJECT = true
	Component.init( self, option )
end

---------------------------------------------------------------------------------

return EditorComponent