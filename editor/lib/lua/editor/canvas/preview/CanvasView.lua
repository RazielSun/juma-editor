
local CoreCanvas = require("canvas.CanvasView")

local AssimpMesh = require("classes.AssimpMesh")
local MeshAnimation = require("classes.MeshAnimation")

local FBXObject = require("classes.FBXMesh")
local OBJObject = require("classes.OBJMesh")

local CanvasDrawGrid = require("canvas.3d.CanvasDrawGrid")
local CanvasLookAtObject = require("canvas.preview.CanvasLookAtObject")

---------------------------------------------------------------------------------
--
-- @type CanvasView
--
---------------------------------------------------------------------------------

local CanvasView = Class( CoreCanvas, "CanvasPreviewView" )

---------------------------------------------------------------------------------
function CanvasView:initCamera()
	local camera = MOAICamera.new()
	camera:setLoc( 0, 0, 500 )
	self.layer:setCamera( camera )
	self:getScene():getLayer():setCamera( camera )
    self.camera = camera
end

function CanvasView:initAddons()
	self.drawGrid = self:add( CanvasDrawGrid { rotate = {90,0,0} } )
	self.nav = self:add( CanvasLookAtObject { camera = self.camera, inputDevice = self.inputDevice } )
end

function CanvasView:initOther()
	local fb = self:getScene():getFrameBuffer()
	if fb then
		fb:setClearDepth( true )
	end

	self:prepareAssimp()
	
	self.nav:setZoom( 1 )
end

---------------------------------------------------------------------------------
function CanvasView:addCanvasItem( item )
end

function CanvasView:removeCanvasItem( item )
end

function CanvasView:changeEditTool( name )
end

function CanvasView:onSelectionChanged( selection )
end

---------------------------------------------------------------------------------
-- NEW SYSTEM
---------------------------------------------------------------------------------
function CanvasView:prepareAssimp()
	self:clearProps()

	self.models = {}
	self.materials = {}

	self.transforms = {}
	self.saveTransforms = {}
end

function CanvasView:createAssimpMesh( node, obj, option )
	local model = AssimpMesh()
	model:setParams( obj )
	model:setNode( node )
	model:setMaterial( self:getMaterial( model:getMaterialID() ) )

	local option = {
		exportMesh = obj.GetExportMesh( obj ),
		exportBuffers = obj.GetExportBuffers( obj ),
		exportBones = false,
		exportMaterialID = false
	}

	model:createMesh( option )
	
	self:addModel ( model )
end

function CanvasView:assimpTransforms( obj, data )
	local name = obj.GetExportName ( obj )

	for tr in python.iter ( data ) do
		local transform = {
			name = tr.name,
			package = name,
			loc = {tr.pos[0],tr.pos[1],tr.pos[2]},
			rot = {tr.rot[0],tr.rot[1],tr.rot[2]},
			scl = {tr.scl[0],tr.scl[1],tr.scl[2]}
		}
		table.insert(self.transforms, transform)
	end

	local canSave = obj.GetExportTransform ( obj )
	if canSave then
		table.insert(self.saveTransforms, name)
	end
end

function CanvasView:assimpMaterials( array )
	for mat in python.iter ( array ) do
		local material = {
			id = mat.id,
			path = mat.path,
			file = mat.file,
			name = mat.name,
		}
		table.insert(self.materials, material)
	end
end

function CanvasView:assimpRender()
	for i, tr in ipairs(self.transforms) do
		local model = self:getModelByName( tr.name )

		if model then
			local mesh = model:getMesh()
			local prop = self:createProp()
			prop:setDeck( mesh )
			prop:setLoc( unpack(tr.loc) )
			prop:setRot( unpack(tr.rot) )
			prop:setScl( unpack(tr.scl) )
		end
	end

	self:updateCanvas()
end

function CanvasView:getModelByName( name )
	local model = nil
	for i, m in ipairs(self.models) do
		if m.name == name then
			model = m
			break
		end
	end
	return model
end

function CanvasView:assimpSave( path )
	if self.models then
		for i, model in ipairs(self.models) do
			if model.canSave then
				local mesh = model:getMesh()
				local data = MOAISerializer.serializeToString ( mesh )
				local fullPath = path .. model.name .. '.mesh'
				MOAIFileSystem.saveFile ( fullPath, data )
			end
		end
	end

	if self.saveTransforms and #self.saveTransforms > 0 then
		for i, trname in ipairs(self.saveTransforms) do
			local tab = {}
			for _, tr in ipairs(self.transforms) do
				if tr.package == trname then
					table.insert(tab, tr)
				end
			end
			local data = Loader:dataToString( tab )
			local fullPath = path .. trname .. '.transform'
			MOAIFileSystem.saveFile(fullPath, "return " .. data)
		end
	end
end

---------------------------------------------------------------------------------
-- Animation
---------------------------------------------------------------------------------
function CanvasView:loadAnimation( path )
	local animation = MeshAnimation( path )
	self.animation = animation

	for _, prop in ipairs(self.props) do
		-- print("loadAnimation:", prop)
		prop:setTexture ( editorAssetPath ( 'grid.png' ) )
		-- prop:setTexture(prop.texture)
		-- prop:setShader( animation.shader )
	end
end

---------------------------------------------------------------------------------
-- PROPS
---------------------------------------------------------------------------------
function CanvasView:createProp()
	local prop = MOAIProp.new()
	prop:setDepthTest( MOAIProp.DEPTH_TEST_LESS ) --DEPTH_TEST_LESS_EQUAL
    prop:setDepthMask(true)
	self.layer:insertProp( prop )
	table.insert( self.props, prop )
	return prop
end

function CanvasView:clearProps()
	if self.props then
		for _, prop in ipairs(self.props) do
			self.layer:removeProp( prop )
		end
	end
	self.props = {}
end

function CanvasView:createPropFromModels()
	for i, model in ipairs(self.models) do
		local prop = self:createProp()
		prop:setDeck( model:getMesh() )
		prop:setLoc( unpack(model.loc) )
		prop:setRot( unpack(model.rot) )
		prop:setScl( unpack(model.scl))
	end
end

---------------------------------------------------------------------------------
function CanvasView:addModel( model )
	table.insert( self.models, model )
end

function CanvasView:clearModels()
	for i, m in ipairs(self.models) do
		self.models[i] = nil
	end
	self.models = {}
end

---------------------------------------------------------------------------------
function CanvasView:getMaterial( id )
	if id then
		for _, mat in ipairs(self.materials) do
			if mat.id == id then
				return mat
			end
		end
	end
	return nil
end

---------------------------------------------------------------------------------
function CanvasView:saveBy( path )
	for i, model in ipairs(self.models) do
		model:save( path )
	end
end

---------------------------------------------------------------------------------

return CanvasView
