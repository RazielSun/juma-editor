
local Entity = require("entity.Entity")

---------------------------------------------------------------------------------
--
-- @type EditorEntity
--
---------------------------------------------------------------------------------

local EditorEntity = Class( Entity, "EditorEntity" )


function EditorEntity:init( option )
	self.FLAG_EDITOR_OBJECT = true
	Entity.init( self, option )
end

---------------------------------------------------------------------------------

return EditorEntity