local Serpent = require("util.Serpent")

local Event = require("input.Event")
local Scene = require("ui.Scene")
local Group = require("ui.Group")
local CanvasToolManager = require("edit.tools.CanvasToolManager")

---------------------------------------------------------------------------------
--
-- @type EditorScene
--
---------------------------------------------------------------------------------

local EditorScene = Class( Scene, "EditorScene" )

---------------------------------------------------------------------------------

local function onDrawBack()
	MOAIGfxDevice.setPenWidth( 1 )
	MOAIGfxDevice.setPenColor( .1, .1, .1, .5 )

	MOAIDraw.drawLine( 0, 1, 0, -1 )
	MOAIDraw.drawLine( 1, 0, -1, 0 )
end

local function onDrawFore()
	MOAIGfxDevice.setPenWidth( 1 )
	MOAIGfxDevice.setPenColor( .1, .1, .1, .5 )

	applyColor 'handle-all'
	MOAIDraw.fillRect( 0, 0, 1, 1 )
end

function EditorScene:init( params )
	params = params or {}
	Scene.init( self, params )

	self.layer = self:addLayer( MOAILayer.new() )
	self.fore = self:addLayer( MOAILayer.new() )

	self.toolManager = CanvasToolManager()
	self.toolManager:addLayer( self.fore )

	self.layer:setUnderlayTable( { onDrawBack } )
	self:createViewport()
	self:createCamera()

	local node = params.rootNode or Group()
	node:setLayer( self.layer )
	self:setActiveGroup( node )
	self.rootNode = node
end

function EditorScene:createCamera()
	local camera = MOAICamera2D.new()
	self.layer:setCamera(camera)
	self.fore:setCamera(camera)
	self.camera = camera
	self.cameraScl = 1
end

function EditorScene:createViewport()
	local viewport = MOAIViewport.new()
	self.layer:setViewport(viewport)
	self.fore:setViewport(viewport)
	self.viewport = viewport
	self.viewWidth = 0
	self.viewHeight = 0
end

function EditorScene:setInputDevice( inputDevice )
	self.inputDevice = inputDevice

	self.inputDevice:addMouseListener( self.mouseEventHandler, self )
	self.inputDevice:addKeyListener( self.keyEventHandler, self )
end

function EditorScene:add( addon )
	local layer = addon.layer
	self:addLayer( layer )
	return addon
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
-- Callbacks
---

function EditorScene:onSelectionChanged( list )
	selection = listToTable( list )
	self.toolManager:onSelectionChanged( selection )
end

function EditorScene:changeEditTool( name )
	self.toolManager:setTool( name )
end

function EditorScene:mouseEventHandler( event )
	if event.type == Event.MOUSE_ENTER or event.type == Event.MOUSE_LEAVE then return end

	local layer = nil
	local prop = nil
	local gameObject = nil
	for i = #self.layers, 1, -1 do
		layer = self.layers[i]
		if layer then
			local lx, ly = layer:wndToWorld( event.x, event.y )
			local prop = self:getTouchableProp( layer, lx, ly )
			if prop and prop.gameObject then
				local breaked = self:handledObjectMouseEvent( prop.gameObject, event )
				if breaked then
					break
				end
			end
		end
	end
end

function EditorScene:keyEventHandler( event )
	print("keyEventHandler", event)
end

-- function EditorScene:getSceneCoords( ex, ey )
-- 	if not ex and not ey then return -99999, -99999 end
-- 	local cx, cy = self.camera:getLoc()
-- 	local vx, vy = self.viewWidth * 0.5, self.viewHeight * 0.5
-- 	local x, y = ex - vx + cx, ey - vy + cy
-- 	return x, y
-- end

-- function EditorScene:notify( group, event )
-- 	local canceled = false
-- 	if group.children then
-- 		local children = group.children
-- 		local child = nil
-- 		for i = #children, 1, -1 do
-- 			child = children[i]
-- 			if child:className() == 'Group' then
-- 				canceled = self:notify( child, event )
-- 			else
-- 				if child.onEvent then
-- 					child:onEvent( event )
-- 					canceled = event.canceled
-- 				end
-- 			end

-- 			if canceled then
-- 				break
-- 			end
-- 		end
-- 	end
-- 	return canceled
-- end

function EditorScene:handledObjectMouseEvent( obj, event )
	local breaked = true
	print("handledObjectMouseEvent:", obj:className(), event.type, event.x, event.y)
	return breaked
end

---------------------------------------------------------------------------------

return EditorScene