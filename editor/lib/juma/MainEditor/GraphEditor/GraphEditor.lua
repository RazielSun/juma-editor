
---------------------------------------------------------------------------------
--
-- @type GraphEditor
--
---------------------------------------------------------------------------------

local GraphEditor = Class("GraphEditor")

---------------------------------------------------------------------------------
function GraphEditor:init()
	-- print("GraphEditor inited")
end

---------------------------------------------------------------------------------
function GraphEditor:getScene()
	return EditorSceneMgr:getCurrentScene()
end

function GraphEditor:getSceneRootNode()
	local scene = EditorSceneMgr:getCurrentScene()
	return scene:getRootNode()
end

function GraphEditor:addEntityByName( entityName )
	local builder = getEntityType( entityName )
	assert( builder )
	local entity = builder()
	self:addEntity( entity )
end

function GraphEditor:addEntity( entity )
	if entity then
		if _owner then
			local scene = self:getScene()
			scene:addEntity( entity )
			_owner.addEntityNode( _owner, entity )
			emitPythonSignal( 'entity.added', entity, 'new' )
		end
	end
end

function GraphEditor:saveScene()
	local scene = self:getScene()
	if scene then
		return LayoutManager:layoutToString( scene:getRootNode() )
	end
	return nil
end

function GraphEditor:loadScene( path )
	local scene = self:getScene()
	if scene then
		local node = LayoutManager:loadByPath( path )
		if node then
			scene:setRootNode( node )
			return node
		end
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
