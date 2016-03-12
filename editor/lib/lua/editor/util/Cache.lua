--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Cache = class()

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Cache:get(key)
    local obj = self.objects[key]
    if not obj then
        obj = self.factory(key)
        self.objects[key] = obj
    end
    return obj
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Cache:init(clazz, weak)
    self.factory = clazz
    self.objects = {}

    if weak then
        setmetatable(self.objects, {__mode = 'v'})
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Cache:set(key, obj)
    self.objects[key] = obj
end

return Cache
