--------------------------------------------------------------------------------
-- File system helpers
--------------------------------------------------------------------------------

local FileSystem = {}

---
-- Returns unique tmp filename given a path
function FileSystem.tmpnam(path)
    local name

    repeat
        local num = math.random(0, 999999)
        name = string.format("%s_%.6d", path, num)
    until not MOAIFileSystem.checkFileExists(name)

    return name
end

---
--
function FileSystem.readFile(path, attempts)
    if not MOAIFileSystem.checkFileExists(path) then
        return
    end

    attempts = attempts or 20
    local dataBuffer = MOAIDataBuffer.new()
    while attempts ~= 0 do
        if dataBuffer:load(path) then
            return dataBuffer:getString()
        end
        attempts = attempts - 1
    end
end


---
-- 
function FileSystem.saveFileAtomic(data, path)
    local tmp = FileSystem.tmpnam(path)
    local dataBuffer = MOAIDataBuffer.new()
    dataBuffer:setString(data)

    if not dataBuffer:save(tmp) then
        MOAIFileSystem.deleteFile(tmp)
        return false
    end

    local status = MOAIFileSystem.rename(tmp, path)
    MOAIFileSystem.deleteFile(tmp)
    return status
end

return FileSystem
