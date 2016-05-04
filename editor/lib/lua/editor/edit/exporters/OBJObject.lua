
local MeshObject = require("edit.exporters.MeshObject")

---------------------------------------------------------------------------------
--
-- @type OBJObject
--
---------------------------------------------------------------------------------

local OBJObject = Class(MeshObject, "OBJObject")

function OBJObject:init()
	MeshObject.init( self )

	self._size = 256
end

---------------------------------------------------------------------------------

return OBJObject
