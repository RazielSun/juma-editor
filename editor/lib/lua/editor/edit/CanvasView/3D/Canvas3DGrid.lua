
local EditorComponent = require("edit.EditorComponent")
local InputEvent = require("input.InputEvent")

---------------------------------------------------------------------------------
--
-- @type Canvas3DGrid
--
---------------------------------------------------------------------------------

local Canvas3DGrid = Class( EditorComponent, "Canvas3DGrid" )

function Canvas3DGrid:init( option )
	option = option or {}
	option.name = option.name or "Canvas3DGrid"

	EditorComponent.init( self, option )
end

---------------------------------------------------------------------------------
function Canvas3DGrid:onLoad()
	self.layer = self.entity.layer
	assert( self.layer )

	self:addMesh()
end

function Canvas3DGrid:getView()
	return self.entity
end

---------------------------------------------------------------------------------
function Canvas3DGrid:addMesh()
	local prop = MOAIProp.new()
	local mesh = self:getMesh()

	prop:setDeck( mesh )
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK )
	prop:setDepthTest( MOAIGraphicsProp.DEPTH_TEST_ALWAYS )

	self.layer:insertProp( prop )
end

function Canvas3DGrid:getMesh()
	local file = MOAIFileSystem.loadFile( editorAssetPath( 'grid.mesh' ) )
    local mesh = assert( loadstring(file) )()

    mesh:setTexture ( editorAssetPath( 'grid.png' ) )

    mesh:setPrimType ( MOAIMesh.GL_LINES )
    mesh:setShader ( MOAIShaderMgr.getShader ( MOAIShaderMgr.MESH_SHADER ) )

	-- @const   GL_POINTS
	-- @const	GL_LINES
	-- @const	GL_TRIANGLES
	-- @const	GL_LINE_LOOP
	-- @const	GL_LINE_STRIP
	-- @const	GL_TRIANGLE_FAN
	-- @const	GL_TRIANGLE_STRIP

	-- @const DECK2D_SHADER
	-- @const DECK2D_SNAPPING_SHADER
	-- @const DECK2D_TEX_ONLY_SHADER
	-- @const FONT_SHADER
	-- @const FONT_SNAPPING_SHADER
	-- @const FONT_EFFECTS_SHADER
	-- @const LINE_SHADER
	-- @const LINE_SHADER_3D
	-- @const MESH_SHADER

    return mesh
end

---------------------------------------------------------------------------------

return Canvas3DGrid
