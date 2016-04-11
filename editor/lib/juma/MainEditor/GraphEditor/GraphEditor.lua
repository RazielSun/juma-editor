
---------------------------------------------------------------------------------
--
-- @type GraphEditor
--
---------------------------------------------------------------------------------

local GraphEditor = Class("GraphEditor")

function GraphEditor:init()
	self.currentScene = nil
end

---------------------------------------------------------------------------------
function GraphEditor:changeScene( scene )
	self.scene = scene
end

function GraphEditor:getScene()
	return self.scene
end

function GraphEditor:getSceneRootGroup()
	if self.scene then
		return self.scene:getRootGroup()
	end
	return nil
end

function GraphEditor:addEntity( entity )
	local scene = self.scene
	if entity and scene then
		
		-- FIXME HARDCODE
		local root = scene:getRootGroup()
		root:addChild( entity )

		if scene.EDITOR_TYPE == "scene" then
			scene:addEntity( entity )
		end

		if scene.EDITOR_TYPE == "ui" then
			_createNodeHelperForUI( entity )
		end

		if scene.camera then
			entity:setLoc( scene.camera:getLoc() )
		end

		if _owner then
			_owner.addEntityNode( _owner, entity )
		end
		emitPythonSignal( 'entity.added', entity, 'new' )
	end
end

function GraphEditor:removeEntity( entity )
	self.scene:removeEntity( entity )
	-- FIXME
	local parent = entity:getParent() or self.scene:getRootGroup()
	parent:removeChild( entity )
end

---------------------------------------------------------------------------------

editor = GraphEditor()

---------------------------------------------------------------------------------

local EditorCommand = require("edit.Command.EditorCommand")

---------------------------------------------------------------------------------
local CmdCreateEntityBase = Class( EditorCommand, "CmdCreateEntityBase" )

function CmdCreateEntityBase:setup( option )
	self.parentEntity = false
end

function CmdCreateEntityBase:redo()
	local entity = self:createEntity()
	if not entity then return false end
	self.created = entity

	if self.parentEntity then
		self.parentEntity:addChild( entity )
	else
		editor:addEntity( entity )
	end
	emitPythonSignal( 'entity.added', self.created, 'new' )
end

function CmdCreateEntityBase:undo()
	self.created:destroy()
	emitPythonSignal( 'entity.removed', self.created )
end

function CmdCreateEntityBase:createEntity()
	return nil
end

function CmdCreateEntityBase:getResult()
	return self.created
end

---------------------------------------------------------------------------------
local CmdCreateEntity = Class( CmdCreateEntityBase, "CmdCreateEntity" )


function CmdCreateEntity:setup( option )
	CmdCreateEntityBase.setup(self, option)
	self.entityName = option.entity
end

function CmdCreateEntity:createEntity()
	local builder = getEntityType( self.entityName )
	assert( builder )
	local e = builder()
	if not e.name then
		e.name = self.entityName
	end
	return e
end

EditorCommand.register( CmdCreateEntity, 'main_editor/create_entity' )

--------------------------------------------------------------------
local CmdCreateComponent = Class( EditorCommand, "CmdCreateComponent" )

function CmdCreateComponent:setup( option )
	self.componentName = option.name	
	local target = getSelection( 'scene' )[1]
	if target:className() ~= 'Entity' then -- FIXME if not isInstance( target, mock.Entity ) then
		return false
	end
	self.targetEntity  = target
end

function CmdCreateComponent:redo()	
	local comType = getComponentType( self.componentName )
	assert( comType )
	local component = comType()
	-- -- if not component:isAttachable( self.targetEntity ) then
	-- -- 	mock_edit.alertMessage( 'todo', 'Group clone not yet implemented', 'info' )
	-- -- 	return false
	-- -- end
	-- component.__guid = generateGUID()
	self.createdComponent = component
	self.targetEntity:add( component )
	-- if component.onEditorInit then
	-- 	component:onEditorInit()
	-- end
	emitPythonSignal( 'component.added', component, self.targetEntity )	
end

function CmdCreateComponent:undo()
	self.targetEntity:remove( self.createdComponent )
	emitPythonSignal( 'component.removed', component, self.targetEntity )	
end

EditorCommand.register( CmdCreateComponent, 'main_editor/create_component' )

--------------------------------------------------------------------
local CmdRemoveEntity = Class( EditorCommand, "CmdRemoveEntity" )

function CmdRemoveEntity:init( option )
	self.selection = getSelection( 'scene' )
	-- self.selection = getTopLevelEntitySelection()-- FIXME 
end

function CmdRemoveEntity:redo()
	for _, target in ipairs( self.selection ) do
		editor:removeEntity( target )
		emitPythonSignal('entity.removed', target )
	end

	-- for _, target in ipairs( self.selection ) do
	-- 	if isInstance( target, mock.Entity ) then
	-- 		if target.scene then 
	-- 			target:destroyWithChildrenNow()
	-- 			gii.emitPythonSignal('entity.removed', target )
	-- 		end
	-- 	elseif isInstance( target, mock.EntityGroup ) then
	-- 		target:destroyWithChildrenNow()
	-- 		gii.emitPythonSignal('entity.removed', target )
	-- 	end
	-- end
end

function CmdRemoveEntity:undo()
	--todo: RESTORE deleted
	-- gii.emitPythonSignal('entity.added', self.created )
end

EditorCommand.register( CmdRemoveEntity, 'main_editor/remove_entity' )
