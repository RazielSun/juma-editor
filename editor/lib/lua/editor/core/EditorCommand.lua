
---------------------------------------------------------------------------------
--
-- @type EditorCommand
--
---------------------------------------------------------------------------------

local EditorCommand = Class( "EditorCommand" )

function EditorCommand.register( clazz, name )
	editorCommandRegistryClass( clazz, name )
	clazz._commandName = name
	-- log.info( 'register Lua Editor Command', name )
end

function EditorCommand:setup( option )
end

---------------------------------------------------------------------------------

function EditorCommand:redo()
end

function EditorCommand:undo()
end

function EditorCommand:canUndo()
	return true
end

function EditorCommand:hasHistory()
	return true
end

function EditorCommand:toString()
	return self._commandName
end

function EditorCommand:getResult()
	return nil
end

---------------------------------------------------------------------------------

return EditorCommand

