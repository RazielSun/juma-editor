--------------------------------------------------------------------------------
-- ImageDownloader.lua
-- 
-- 
-- 
--------------------------------------------------------------------------------

local ResourceMgr = require("core.ResourceMgr")
local HttpTask = MOAIHttpTaskNSURL or MOAIHttpTask or Mock("HttpTask mock")

local ImageDownloader = {}

local MAX_TASKS = 5
local ActiveDownloadTasks = setmetatable({}, {__mode = "v"})

-- Curl uses "overall process" timeout, and can kill valid tasks still transfering data.
-- NSURL uses "idle timeout", the time from last actual data transfer which is more expected.
-- 
-- MOAI have default of 15 seconds for both. 
-- We alter it slightly to give curl a bit more time to finish task. 
local TIMEOUT = MOAIHttpTaskNSURL and 15 or 45


-- manager for concurrent tasks
local httpTaskQueue = {}
local imageUpdateQueue = {}
local thread = MOAICoroutine.new()


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.affirmThread()
    if not thread:isBusy() then
        thread:run(ImageDownloader.update)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.cancelTask(url, path)
    -- remove task from waiting queue;
    -- or if it is already running, then don't apply deck image on finish
    local idx
    for i, t in ipairs(httpTaskQueue) do
        if t[1] == url and t[2] == path then
            idx = i
            break
        end
    end
    if idx then
        table.remove(httpTaskQueue, idx)
    end

    local task = ActiveDownloadTasks[url]
    if task then
        -- if task.cancel then
        --     task:cancel()
        --     task:setCallback()
        -- end
        ActiveDownloadTasks[url] = nil
        task.cancelled = true
    end

    for _, t in pairs(imageUpdateQueue) do
        if t[2] == path then
            t[5] = true
        end
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.pushHttpTask(url, path, onFinish, userdata)
    if not url or ActiveDownloadTasks[url] then
        return
    end

    table.insert(httpTaskQueue, {url, path, onFinish, userdata})
    ImageDownloader.affirmThread()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.pushUpdateImage(data, path, onFinish, userdata, cancelled)
    table.insert(imageUpdateQueue, {data, path, onFinish, userdata, cancelled})
    ImageDownloader.affirmThread()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.startHttpTask(url, path, onFinish, userdata)
    if ActiveDownloadTasks[url] then return end

    local task = HttpTask.new()

    task:setVerb(HttpTask.HTTP_GET)
    task:setUrl(url)
    task:setUserAgent("Moai")
    task:setTimeout(TIMEOUT)
        
    task.cancelled = false
    task:setCallback(function(t, responseCode)
        local data = t:getString()
        if t:getProgress() == 1 then
            -- t:saveFile(path)
            ImageDownloader.pushUpdateImage(data, path, onFinish, userdata, t.cancelled)
        end
        ActiveDownloadTasks[url] = nil
    end)
    
    task:performAsync()

    ActiveDownloadTasks[url] = task
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.startImageUpdate(data, path, onFinish, userdata, cancelled)
    local buf = MOAIDataBuffer.new()
    buf:setString(data)

    local image = MOAIImage.new()
    image:loadFromBuffer(buf)

    -- fix grayscale jpegs (MOAI treats them as A8 images, instead of L8)
    if image:getFormat() == MOAIImage.COLOR_FMT_A_8 then
        image = image:convert ( MOAIImage.COLOR_FMT_RGBA_8888 )
        image:mix (
            0, 0, 0, 1,
            0, 0, 0, 1,
            0, 0, 0, 1,
            0, 0, 0, 1
        )
        
        -- copy image into new buffer to get rid of any possible alpha
        local w, h = image:getSize()
        local output = MOAIImage.new ()
        output:init ( w, h, MOAIImage.COLOR_FMT_RGBA_8888 )
        output:fillRect ( 0, 0, w, h, 0, 0, 0, 1 )
        output:copyRect ( 
            image, 0, 0, w, h, 0, 0, w, h, 
            MOAIImage.FILTER_NEAREST, MOAIImage.BLEND_FACTOR_1110, MOAIImage.BLEND_FACTOR_0001, MOAIImage.BLEND_EQ_ADD
        )
        image = output

        -- save as png
        image:writePNG(path)
    else
        buf:save(path)
    end
    
    if onFinish then
        if userdata then
            onFinish(userdata, image, cancelled)
        else
            onFinish(image, cancelled)
        end
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ImageDownloader.update()
    local task
    repeat
        local count = 0
        for _, t in pairs(ActiveDownloadTasks) do
            if t:isBusy() then
                count = count + 1
            end
        end

        if count < MAX_TASKS then
            task = table.remove(httpTaskQueue, 1)
            if task then
                ImageDownloader.startHttpTask(unpack(task))
                coroutine.yield()
            end
        end

        task = table.remove(imageUpdateQueue, 1)
        if task then
            ImageDownloader.startImageUpdate(unpack(task))
            coroutine.yield()
        end

        coroutine.yield()
    until #httpTaskQueue == 0 and #imageUpdateQueue == 0
end


return ImageDownloader
