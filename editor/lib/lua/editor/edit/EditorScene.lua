
local InputEvent = require("input.InputEvent")
local Scene = require("scenes.Scene")
local Widget = require("ui.Widget")
local CanvasToolManager = require("edit.tools.CanvasToolManager")
local FrameScene = require("edit.tools.FrameScene")
local CanvasGrid = require("edit.tools.CanvasGrid")

---------------------------------------------------------------------------------
--
-- @type EditorScene
--
---------------------------------------------------------------------------------

local EditorScene = Class( Scene, "EditorScene" )

function EditorScene:init( params )
	params = params or {}
	Scene.init( self, params )

	self.framelayer = self:addLayer()
	-- self.gridlayer = self:addLayer()
	self.layer = self:addLayer()
	self.foreground = self:addLayer()

	self.toolManager = CanvasToolManager( self.foreground, self.layer )
	self.frameScene = FrameScene( self.framelayer )
	-- self.grid = CanvasGrid( self.gridlayer )
	self:createViewport()

	local camera = MOAICamera2D.new()
	self.framelayer:setCamera(camera)
	self.layer:setCamera(camera)
	self.foreground:setCamera(camera)
	self.camera = camera

	self.cameraScl = 1
	self.maxCameraScl = 3
	self.minCameraScl = 0.1
	self.cameraSclStep = 0.1

	local node = params.rootNode or Widget()
	node:setLayer( self.layer )
	self:setActiveGroup( node )
	self.rootNode = node
end

function EditorScene:createViewport()
	local viewport = MOAIViewport.new()
	for _, layer in ipairs(self.layers) do
		layer:setViewport(viewport)
	end
	self.viewport = viewport
	self.viewWidth = 0
	self.viewHeight = 0
end

function EditorScene:setInputDevice( inputDevice )
	self.inputDevice = inputDevice

	self.inputDevice:addMouseListener( self.mouseEventHandler, self )
	self.inputDevice:addKeyListener( self.keyEventHandler, self )
end

---------------------------------------------------------------------------------
function EditorScene:resize( w, h )
	self.viewport:setSize(w,h)
	self.viewport:setScale(w,h)

	self.viewWidth, self.viewHeight = w, h
end

function EditorScene:updateCanvas()
	self.env.updateCanvas()
end

function EditorScene:cameraZoom( zoom_type )
	local maxed = false
	if zoom_type then
		local scl = self.cameraScl
		if zoom_type == 'normal' then
			scl = 1
		elseif zoom_type == 'in' then
			scl = scl - self.cameraSclStep
			maxed = scl <= self.minCameraScl
		elseif zoom_type == 'out' then
			scl = scl + self.cameraSclStep
			maxed = scl >= self.maxCameraScl
		end

		scl = math.clamp( scl, self.minCameraScl, self.maxCameraScl)
		self.cameraScl = scl

		self.camera:setScl( scl, scl, scl )
	end
	return maxed
end

function EditorScene:showGrid( show )
	--
end

function EditorScene:resizeFrame( width, height )
	self.frameScene:resize( width, height )
end

function EditorScene:goToPos( x, y )
	self.camera:setLoc( x, y )
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

function EditorScene:addEntity( entity )
	entity:setLoc( self.camera:getLoc() )
	self.activeGroup:addChild( entity )
end

function EditorScene:removeEntity( entity )
	return self:removeWidget( entity, self.activeGroup )
end

function EditorScene:removeWidget( widget, group )
	local success = false

	for _, child in ipairs(group.children) do
		if child == widget then
			success = true
		end

		if success then
			break
		end
	end

	if success then
		widget:removeChildren()
		group:removeChild( widget )
	end

	return success
end


---------------------------------------------------------------------------------
-- function CanvasView:pickAndSelect( x, y, pad )
-- 	local picked = self:pick( x, y, pad )
-- 	gii.changeSelection( 'scene', unpack( picked ) )
-- 	return picked
-- end
function EditorScene:changeSelection( picked )
	changeSelection( 'scene', unpack(picked) )
end

---------------------------------------------------------------------------------
-- Callbacks
---

function EditorScene:onSelectionChanged( list )
	selection = listToTable( list )
	self.toolManager:onSelectionChanged( selection )
	self:updateCanvas()
end

function EditorScene:changeEditTool( name )
	self.toolManager:setTool( name )
end

function EditorScene:mouseEventHandler( event )
	if event.eventName == InputEvent.MOUSE_ENTER or event.eventName == InputEvent.MOUSE_LEAVE then return end

	local intercept = self.toolManager:onMouseEvent( event )

	if not intercept then
		-- FIXME this is self.toolManager.toolId == 'select_object'
		if event.eventName == InputEvent.MOUSE_UP then
			local layer = nil
			local prop = nil
			local finded = false
			for i = #self.layers, 1, -1 do
				layer = self.layers[i]
				if layer then
					local lx, ly = layer:wndToWorld( event.x, event.y )
					prop = self:getProp( layer, lx, ly, false )
					if prop and prop.gameObject then
						finded = true
						self:changeSelection( { prop.gameObject } )
						break
					end
				end
			end

			if not finded then
				self:changeSelection( {} )
			end
		end
	end
end


function EditorScene:keyEventHandler( event )
	-- print("keyEventHandler", event)
end

function EditorScene:handledObjectMouseEvent( obj, event )
	local breaked = true
	-- print("handledObjectMouseEvent:", obj:className(), event.type, event.x, event.y)
	return breaked
end

---------------------------------------------------------------------------------

return EditorScene