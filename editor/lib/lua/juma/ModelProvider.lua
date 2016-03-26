----------------------------------------------------------------------
----MODEL
----------------------------------------------------------------------

local bridge = PYTHON_BRIDGE
local modelBridge = bridge.ModelBridge.get()

----------------------------------------------------------------------
--
local function createPyModel( model )
	local pmodel = modelBridge:newLuaObjectModel( model.__name )

	local fields = model:getFieldList( true )
	for i, f in ipairs( fields ) do
		local option = {
			get   = f.__getter,
			set   = f.__setter,
			label = f.__label,
			meta  = f.__meta
		}
		local id     = f.__id
		local typeid = f.__type
		local meta 	 = f.__meta

		if meta then
			for key, value in pairs(meta) do
				option[key] = value
			end
		end

		if typeid == '@enum' then
			if type(f.__itemtype) == 'table' then
				pmodel:addLuaEnumFieldInfo( id, f.__itemtype, option )
			else
				_error('invalid enum type')
			end
		elseif typeid == "@asset" then
			pmodel:addLuaAssetFieldInfo( id, f.__itemtype, option )
		else
			pmodel:addLuaFieldInfo( id, typeid, option )
		end
	end

	model.__py_model = pmodel
	return pmodel
end

----
local function typeIdGetter( obj )
	local tt = type(obj)
	if tt == 'table' then
		if isClass(obj) then
			return obj:className()
		end
	elseif tt == 'userdata' then
		local getClass = obj.getClass
		if getClass then
			return getClass(obj)
		end
	end
	return nil
end

----
local function modelGetter( obj )
	local model
	local tt = type(obj)

	if tt == 'table' then
		local clazz = obj -- getmetatable(obj)
		if not isClass( obj ) then return nil end
		model = Model.fromClass( clazz )
	-- elseif tt == 'userdata' then --MOAIObject
	-- 	local getClass = obj.getClass
	-- 	if getClass then
	-- 		local clas = getClass( obj )
	-- 		model = MoaiModel.fromClass( clas )
	-- 	end
	else
		return nil
	end

	if not model then
		return nil
	end

	local pyModel = model.__py_model
	if not pyModel then
		pyModel = createPyModel( model )
	end
	
	return pyModel
end

----
local function modelFromType( t )
	local clazz = getClassByName( t )
	local model = Model.fromClass( clazz )
	if not model then
		return nil
	end	

	local pyModel = model.__py_model
	if not pyModel then
		pyModel = createPyModel( model )
	end
	return pyModel
end

----
registerModelProvider {
	name               = 'ModelProvider',
	priority           = 100,
	getTypeId          = typeIdGetter,
	getModel           = modelGetter,
	getModelFromTypeId = modelFromType
}