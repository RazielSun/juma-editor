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
	MOAIGfxDevice.setPenColor( .1, .1, .1, .5 )

	MOAIDraw.drawLine( 0, 1, 0, -1 )
	MOAIDraw.drawLine( 1, 0, -1, 0 )
end

function EditorScene:init( params )
	params = params or {}

	local backlayer = MOAILayer.new()
	local layer = MOAILayer.new()
	local forelayer = MOAILayer.new()

	backlayer:setUnderlayTable( { onDrawBack } )
	self.renderTable = { backlayer, layer, forelayer }
	self:createViewport()
	self:createCamera()

	local rootNode = params.rootNode or Group()
	rootNode:setLayer( layer )
	self:setActiveGroup( rootNode )

	self.layer = layer
	self.forelayer = forelayer
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

function EditorScene:setInputDevice( inputDevice )
	self.inputDevice = inputDevice

	local function inputHandler( event )
		self:inputDeviceHandler( event )
	end

	inputDevice:addListener( inputHandler )
end

---------------------------------------------------------------------------------

function EditorScene:inputDeviceHandler( event )
	if self.rootNode then
		event.wx, event.wy = self:getSceneCoords( event.x, event.y )
		self:notify( self.rootNode, event )
	end
end

function EditorScene:getSceneCoords( ex, ey )
	if not ex and not ey then return -99999, -99999 end
	local cx, cy = self.camera:getLoc()
	local vx, vy = self.viewWidth * 0.5, self.viewHeight * 0.5
	local x, y = ex - vx + cx, ey - vy + cy
	return x, y
end

function EditorScene:notify( group, event )
	local canceled = false
	if group.children then
		local children = group.children
		local child = nil
		for i = #children, 1, -1 do
			child = children[i]
			if child:className() == 'Group' then
				canceled = self:notify( child, event )
			else
				if child.onEvent then
					child:onEvent( event )
					canceled = event.canceled
				end
			end

			if canceled then
				break
			end
		end
	end
	return canceled
end

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