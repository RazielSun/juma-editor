
local CoreCanvas = require("canvas.CanvasView")

local AssimpMesh = require("classes.AssimpMesh")
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
	self.transforms = {}
	self.namesTransforms = {}
end

function CanvasView:createAssimpMesh( node, obj )
	local size = obj.GetPerPixel( obj )
	local texture = obj.GetTexture( obj, true )

	local model = AssimpMesh( size, texture )
	model:setNode( node )
	
	self:addModel( model )
end

function CanvasView:assimpTransforms( name, data )
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

	table.insert(self.namesTransforms, name)
end

function CanvasView:assimpRender()
	for i, tr in ipairs(self.transforms) do
		local model = self:getModelByName( tr.name )
		if model then
			local prop = self:createProp()
			prop:setDeck( model:getMesh() )
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
			local mesh = model:getMesh()
			local data = MOAISerializer.serializeToString(mesh)
			local fullPath = path .. model.name .. '.mesh'
			MOAIFileSystem.saveFile(fullPath, data)
		end
	end

	if self.namesTransforms and #self.namesTransforms > 0 then
		for i, trname in ipairs(self.namesTransforms) do
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
-- OLD FBX OBJ system
---------------------------------------------------------------------------------
function CanvasView:createProp()
	local prop = MOAIProp.new()
	prop:setCullMode ( MOAIGraphicsProp.CULL_BACK ) --CULL_FRONT ) --
	prop:setDepthTest( MOAIGraphicsProp.DEPTH_TEST_LESS ) --DEPTH_TEST_LESS_EQUAL
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
function CanvasView:createModel( node, params )
	print("createModel", node, params)
	local ftype = params.GetFormat( params )
	if ftype == 'FBX' then
		self:renderFBX( node, params )
	elseif ftype == 'OBJ' then
		self:renderOBJ( node, params )
	end
end

---------------------------------------------------------------------------------
function CanvasView:renderNode( node, params )
	self:clearModels()
	self:createModel( node, params )

	self:clearProps()
	self:createPropFromModels()

	self:updateCanvas()
end

function CanvasView:renderFBX( rootNode, obj )
	local size = obj.GetPerPixel( obj )
	local texture = obj.GetTexture( obj, true )

	self:createMeshFromFBX( rootNode, rootNode, size, texture )
end

function CanvasView:createMeshFromFBX( node, rootNode, size, texture )
	if not node then return end
	
	local total = node.GetChildCount()

	for i = 0, total-1 do
		local child = node.GetChild(i)
		print("CHILD:", child, child.GetName())
		local totalChilds = child.GetChildCount()
		if totalChilds > 0 then
			self:createMeshFromFBX( child, rootNode, size, texture )
		else
			local mesh = child.GetMesh()
			if mesh then
				print("   mesh:", mesh)
				local model = FBXObject( size, texture )
				model:setFBXMaterials( child, rootNode.FbxLayerElement )
				model:setNode( child )
				model:createMesh()
				self:addModel( model )
			end
		end
	end
end

function CanvasView:renderOBJ( node, obj )
	local size = obj.getPerPixel( obj )

	local model = OBJObject( size )
	model:setOBJMaterials( node )
	model:setNode( node )
	model:createMesh()

	self:addModel( model )
end

---------------------------------------------------------------------------------
function CanvasView:saveBy( path )
	for i, model in ipairs(self.models) do
		model:save( path )
	end
end

---------------------------------------------------------------------------------

return CanvasView
