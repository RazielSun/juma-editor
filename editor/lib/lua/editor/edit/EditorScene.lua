local Serpent = require("util.Serpent")

local Layout = require("core.Layout")
local Group = require("ui.Group")

---------------------------------------------------------------------------------
--
-- @type EditorScene
--
---------------------------------------------------------------------------------

local EditorScene = Class( Layout, "EditorScene" )

---------------------------------------------------------------------------------

local function onDrawBack()
	MOAIGfxDevice.setPenWidth( 1 )
	MOAIGfxDevice.setPenColor( .2, .2, .2, .5 )

	MOAIDraw.drawLine( 0, 1, 0, -1 )
	MOAIDraw.drawLine( 1, 0, -1, 0 )
end

function EditorScene:init( params )
	params = params or {}

	local layer = MOAILayer.new()
	local overlay = MOAILayer.new()
	local backlayer = MOAILayer.new()

	backlayer:setUnderlayTable( { onDrawBack } )
	self.renderTable = { backlayer, layer, overlay }
	self:createViewport()
	self:createCamera()

	local rootNode = params.rootNode or Group()
	rootNode:setLayer( layer )
	self:setActiveGroup( rootNode )

	self.layer = layer
	self.overlay = overlay
	self.backlayer = backlayer
	self.rootNode = rootNode
end

function EditorScene:createCamera()
	local camera = MOAICamera2D.new()
	for _, layer in ipairs(self.renderTable) do
		layer:setCamera(camera)
	end
	self.camera = camera
	self.cameraScl = 1
end

function EditorScene:createViewport()
	local viewport = MOAIViewport.new()
	
	for _, layer in ipairs(self.renderTable) do
		layer:setViewport(viewport)
	end
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

function EditorScene:addWidgetToActiveGroup( widget )
	self.activeGroup:addChild( widget )
end

function EditorScene:removeWidgetToActiveGroup( widget )
	return self:removeWidget( widget, self.activeGroup )
end

function EditorScene:removeWidget( widget, group )
	local success = false

	for _, child in ipairs(group.children) do
		if child == widget then
			success = true
		elseif child:className() == 'Group' then
			success = self:removeWidget( widget, child )
		end
		if success then
			break
		end
	end

	if success then
		group:removeChild( widget )
	end

	return success
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