--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local Async = {}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
local function appendHelper(a, n, b, ...)
    if n == 0 then
        return a
    else
        return b, appendHelper(a, n - 1, ...)
    end
end

local function append(a, ...)
    return appendHelper(a, select('#', ...), ...)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
local function _timeout(self, time)
    if not self.timer then
        self.timer = MOAITimer.new()
    end
    local timer = self.timer
    timer:setSpan(time)
    timer:start()

    return self
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
local function _wrap(self, func, ...)
    local coro = self.thread
    local timer = self.timer
    local async, results = true, nil
    local timeout = false

    if timer and timer:isActive() then
        timer:setListener(MOAIAction.EVENT_STOP, function()
            coroutine.resume(coro)
            timeout = true
        end)
    end

    local function callback(...)
        if timeout then log.warning("Callback called after timeout, ignoring") return end
        -- this is to ensure that callback is called exaclty once
        timeout = true
        if timer then
            timer:setListener(MOAIAction.EVENT_STOP)
            timer:stop()
        end
        if coro ~= coroutine.running() then
            local success, err = coroutine.resume(coro, ...)
            if not success then
                Async.tracebackHandler(err, coro)
            end
        else
            async = false
            results = {...}
        end
    end

    func(append(callback, ...))
    if async then
        return coroutine.yield()
    else
        return unpack(results)
    end
end

local async_mt = {__call = _wrap}

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function Async.start(func, onFinish)
    local async = {}
    local threadFunc = func
    if onFinish then
        threadFunc = function(wrap) onFinish(func(wrap)) end
    end

    async.thread = coroutine.create(threadFunc)
    async.timeout = function(time)
        return _timeout(async, time)
    end

    setmetatable(async, async_mt)

    local success, err = coroutine.resume(async.thread, async)
    if not success then
        Async.tracebackHandler(err, async.thread)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- reimplement if needed
function Async.tracebackHandler(err, thread)
    log.critical(debug.traceback(thread, err))
end


return setmetatable(Async, Async)
