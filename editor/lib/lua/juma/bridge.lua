--------------------------------------------------------------------
-- Bridge
--------------------------------------------------------------------

local bridge = PYTHON_BRIDGE

sizeOfPythonObject  = bridge.sizeOfPythonObject
appendPythonList 	= bridge.appendPythonList
newPythonList 		= bridge.newPythonList

emitPythonSignal   	= bridge.emitPythonSignal
emitPythonSignalNow = bridge.emitPythonSignalNow

-- hardcode register assets in moai
registerAssetNodeInLibrary = bridge.registerAssetNodeInLibrary

--------------------------------------------------------------------
function dictToTablePlain( dict )
	local t = {}
	for k in python.iter( dict ) do
		t[k] = dict[k]
	end
	return t	
end

--data conversion
local encodeDict = bridge.encodeDict
local decodeDict = bridge.decodeDict

function tableToDict( table )
	local json = MOAIJsonParser.encode(table)
	return decodeDict( json )
end

function tableToList(table)
	local list = newPythonList()
	if table then
		for i, v in ipairs(table) do
			appendPythonList(list,v)
		end
	end
	return list
end

local _sizeOf = sizeOfPythonObject
function listToTable( list )
	local c=_sizeOf( list )
	local r={}
	for i = 1, c do
		r[i]=list[i-1]
	end
	return r
end

--------------------------------------------------------------------
-- EDITOR RELATED
--------------------------------------------------------------------
function changeSelection( key, obj, ... )
	assert( type(key)=='string', 'selection key expected' )
	if obj then
		bridge.changeSelection( key, newPythonList(obj,...) )
	else
		bridge.changeSelection( key, nil )
	end
end

function addSelection( key, obj, ... )
	assert( type(key)=='string', 'selection key expected' )
	if obj then
		bridge.addSelection( key, newPythonList(obj,...) )
	else
		bridge.addSelection( key, nil )
	end
end

function removeSelection( key, obj, ... )
	assert( type(key)=='string', 'selection key expected' )
	if obj then
		bridge.removeSelection( key, newPythonList(obj,...) )
	else
		bridge.removeSelection( key, nil )
	end
end

function toggleSelection( key, obj, ... )
	assert( type(key)=='string', 'selection key expected' )
	if obj then
		bridge.toggleSelection( key, newPythonList(obj,...) )
	else
		bridge.toggleSelection( key, nil )
	end
end

function getSelection( key )
	assert( type(key)=='string', 'selection key expected' )
	return listToTable( bridge.getSelection( key ) )
end

app = bridge.app

function getProject()
	return app:getProject()
end

function getApp()
	return app
end

--------------------------------------------------------------------
-- PYTHON-LUA DELEGATION CREATION
--------------------------------------------------------------------
function loadLuaDelegate(file, env, ...)
	if env then
		assert ( type( env ) == 'userdata' )
		env = dictToTablePlain( env )
	end

	env = setmetatable(env or {}, 
			{__index=function(t,k) return rawget(_G,k) end}
		)
	local func, err=loadfile(file)
	if not func then
		error('Failed load script:'..file..'\n'..err, 2)
	end

	setfenv(func, env)
	local args = {...}
	
	local function _f()
		return func( unpack( args ))
	end

	local function _onError( err, level )
		print ( err )
		print( debug.traceback( level or 2 ) )
		return err, level
	end

	local succ, err = xpcall( _f, _onError )
	if not succ then
		error('Failed start script:'.. file, 2)
	end

	return env
end

--------------------------------------------------------------------
-- CTHelper methods
--------------------------------------------------------------------

assert(CTHelper.stepSim, "CTHelper stepSim is NULL")
assert(CTHelper.setBufferSize, "CTHelper setBufferSize is NULL")
assert(CTHelper.renderFrameBuffer, "CTHelper renderFrameBuffer is NULL")

local renderFrameBuffer = CTHelper.renderFrameBuffer

function renderTable( t )
	for _, item in ipairs(t) do
		local itemType = type(item)
		if itemType == 'table' then
			renderTable( item )
		elseif itemType == 'userdata' then
			renderFrameBuffer( item )
		end
	end
end

local setBufferSize = CTHelper.setBufferSize

function setBufferSizeForTable( t, width, height )
	for _, item in ipairs(t) do
		local itemType = type(item)
		if itemType == 'table' then
			setBufferSizeForTable( item, width, height )
		elseif itemType == 'userdata' then
			setBufferSize( item, width, height )
		end
	end
end

local stepSim = CTHelper.stepSim

function updateStepSim( step )
	stepSim( step )
end

--------------------------------------------------------------------
-- MODEL
--------------------------------------------------------------------
local modelBridge = bridge.ModelBridge.get()

function registerModelProvider( setting )
	local name      		  = setting.name
	local priority 			  = setting.priority or 10
	local getTypeId           = assert( setting.getTypeId, 'getTypeId not provided' )
	local getModel            = assert( setting.getModel,  'getModel not provided' )
	local getModelFromTypeId  = assert( setting.getModelFromTypeId,  'getModelFromTypeId not provided' )
	return modelBridge:buildLuaObjectModelProvider( 
			name, priority, getTypeId, getModel, getModelFromTypeId
		)
end

--------------------------------------------------------------------
-- Editor Command
--------------------------------------------------------------------
registerLuaEditorCommand = bridge.registerLuaEditorCommand
doCommand = bridge.doCommand
undoCommand = bridge.undoCommand

--------------------------------------------------------------------

return Bridge