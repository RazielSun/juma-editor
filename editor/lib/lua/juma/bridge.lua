--------------------------------------------------------------------
-- Bridge
--------------------------------------------------------------------

local bridge = PYTHON_BRIDGE

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

return Bridge