local Serpent = require("util.Serpent")

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
	self:setActiveGroup( rootNode )

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

function EditorScene:setRootNode( node )
	if self.rootNode == node then return end

	if self.rootNode then
		self.rootNode:removeChildren()
		self.rootNode:setLayer( nil )
		self.rootNode = nil
	end

	if node then
		node:setLayer( self.layer )
		self.rootNode = node
		self:setActiveGroup( node )
	end
end

function EditorScene:setActiveGroup( node )
	self.activeGroup = node
end

function EditorScene:addNodeToActiveGroup( node )
	self.activeGroup:addChild( node )
end

---------------------------------------------------------------------------------

function EditorScene:save()
	return Serpent.pretty( serialize( self.rootNode ), { comment = false } )
end

function EditorScene:load( path )
	if path then
		data = dofile(path)
		if data then
			node = deserialize( nil, data )

			if node then
				self:setRootNode( node )
			end
		end
	end
end

---------------------------------------------------------------------------------

return EditorScene