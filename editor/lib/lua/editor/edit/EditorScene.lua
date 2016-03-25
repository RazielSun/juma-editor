
local InputEvent = require("input.InputEvent")
local Scene = require("scenes.Scene")
local Widget = require("ui.Widget")
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

function EditorScene:init( params )
	params = params or {}
	Scene.init( self, params )

	self.background = self:addLayer()
	self.layer = self:addLayer()
	self.toolManager = self:add( CanvasToolManager() )

	self.background:setUnderlayTable( { onDrawBack } ) --# FIXME
	self:createViewport()
	self:createCamera()

	local node = params.rootNode or Widget()
	node:setLayer( self.layer )
	self:setActiveGroup( node )
	self.rootNode = node
end

function EditorScene:createCamera()
	local camera = MOAICamera2D.new()
	for _, layer in ipairs(self.layers) do
		layer:setCamera(camera)
	end
	self.camera = camera
	self.cameraScl = 1
	self.maxCameraScl = 3
	self.minCameraScl = 0.1
	self.cameraSclStep = 0.1
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
	if event.type == InputEvent.MOUSE_ENTER or event.type == InputEvent.MOUSE_LEAVE then return end

	local intercept = self.toolManager:onMouseEvent( event )

	if not intercept then
		if event.type == InputEvent.MOUSE_UP and self.toolManager.toolId == 'select_object' then
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
						emitPythonSignal( 'selection.target', tableToList( {prop.gameObject} ), 'scene' )
						break
					end
				end
			end

			if not finded then
				emitPythonSignal( 'selection.target', tableToList( {} ), 'scene' )
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