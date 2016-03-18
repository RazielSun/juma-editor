
local function typeIdGetter(v)
	local tt = type(v)
	if tt == 'table' then
		local mt = getmetatable(v)
		if not mt then return nil end
		return mt
	elseif tt == 'userdata' then
		local getClass = v.getClass
		if getClass then
			return getClass(v)
		end
	end
	
	return nil
end

local function modelGetter(o)
	return nil
end

local function modelFromType(t)
	return nil
end

registerModelProvider {
	name               = 'MOAIModelProvider',
	priority           = 10,
	getTypeId          = typeIdGetter,
	getModel           = modelGetter,
	getModelFromTypeId = modelFromType
}