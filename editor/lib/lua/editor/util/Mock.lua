--------------------------------------------------------------------------------
-- Mock.lua
--
--
--------------------------------------------------------------------------------

---
-- Mock object that allow calling and indexing any values without exceptions
-- Returns itself on indexing, so calls can be chained
-- Can print accesses for debug purposes

local Mock = {}
local mt = {}

function Mock:__call(name, verbose, preset)
    local mock = table.dup(mt)
    mock.name = name or "mock"
    mock.verbose = verbose or false
    mock.preset = {}
    if preset then
        for k,v in pairs(preset) do
            mock.preset[k] = function() return v end
        end
    end
    mock.__index = self.__index
    mock.__newindex = self.__newindex
    mock.__call = function(m) return m end
    setmetatable(mock, mock)
    return mock
end

function Mock:__index(key)
    if self.verbose then
        print(self.name .. ": " .. tostring(key))
    end
    return self.preset[key] or self
end

function Mock:__newindex(key, value)
    if self.verbose then
        print(self.name .. ' assigned: ' .. tostring(value) .. ' to ' .. tostring(key))
    end
end

local function arith(a, b)
    if type(a) == "number" then
        return a
    elseif type(b) == "number" then
        return b
    else
        return 0
    end
end

mt.__add = arith
mt.__sub = arith
mt.__mult = arith
mt.__div = arith

setmetatable(Mock, Mock)

return Mock