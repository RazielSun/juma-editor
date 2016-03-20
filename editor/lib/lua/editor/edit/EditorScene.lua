local Layout = require("core.Layout")
local EntityGroup = require("core.EntityGroup")

---------------------------------------------------------------------------------
--
-- @type EditorScene
--
---------------------------------------------------------------------------------

local EditorScene = Class( Layout, "EditorScene" ):FIELDS{
	Field("rootNode")	:object()	:getset("RootNode")	:label("RootNode");
}

---------------------------------------------------------------------------------

function EditorScene:init( params )
	params = params or {}

	local layer = MOAILayer.new()
	local camera = MOAICamera2D.new()
	local viewport = MOAIViewport.new()

	layer:setViewport(viewport)
	layer:setCamera(camera)

	local rootNode = params.rootNode or EntityGroup()
	rootNode:setLayer( layer )

	self.layer = layer
	self.rootNode = rootNode
	self.camera = camera
	self.cameraScl = 1
	self.viewport = viewport
	self.viewWidth = 0
	self.viewHeight = 0
end

---------------------------------------------------------------------------------

function EditorScene:resize( w, h )
	self.viewport:setSize(w,h)
	self.viewport:setScale(w,h)

	self.viewWidth, self.viewHeight = w, h
end

---------------------------------------------------------------------------------

function EditorScene:getRootNode()
	return self.rootNode
end

function EditorScene:setRootNode( rootNode )
	if self.rootNode == rootNode then return end

	if self.rootNode then
		self.rootNode:setLayer( nil )
		self.rootNode = nil
	end

	if rootNode then
		rootNode:setLayer( layer )
		self.rootNode = rootNode
	end
end

---------------------------------------------------------------------------------

function EditorScene:save()
	return serialize( self )
end

function EditorScene:load( data )
	deserialize( self, data )
end

---------------------------------------------------------------------------------

return EditorScene