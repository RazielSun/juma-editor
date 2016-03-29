
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

function GraphEditor:getSceneRootNode()
	return self.scene:getRootGroup()
end

function GraphEditor:addEntityByName( entityName )
	local builder = getEntityType( entityName )
	assert( builder )
	local entity = builder()
	self:addEntity( entity )
end

function GraphEditor:addEntity( entity )
	local scene = self.scene
	if entity then
		local root = scene:getRootGroup()
		root:addChild( entity )

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
end

function GraphEditor:saveSceneAs( path )
	local scene = self.scene
	if scene then
		return EntityManager:save( path, scene:getRootGroup() )
	end
	return nil
end

function GraphEditor:openScene( path )
	local scene = self:getScene()
	if scene then
		local group = EntityManager:load( path )
		if group then
			scene:setRootGroup( group )
		end
		return scene
	end
	return nil
end

function GraphEditor:openSceneAs( path )
	local scene = self:getScene()
	if scene then
		local group = EntityManager:loadByPath( path )
		if group then
			scene:setRootGroup( group )
		end
		return scene
	end
	return nil
end

---------------------------------------------------------------------------------

editor = GraphEditor()

local EditorCommand = require("edit.Command.EditorCommand")

---------------------------------------------------------------------------------
--
-- @type CmdCreateEntityBase
--
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
--
-- @type CmdCreateEntityBase
--
---------------------------------------------------------------------------------

local CmdCreateEntity = Class( CmdCreateEntityBase, "CmdCreateEntity" )

function CmdCreateEntity:setup( option )
	CmdCreateEntityBase.setup(self, option)
	self.entityName = option.name
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

-- EditorCommand.register( CmdCreateEntity, 'main_editor/create_entity' )
