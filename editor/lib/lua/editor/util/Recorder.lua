--------------------------------------------------------------------------------
-- Recorder.lua
-- 
-- Log all events (input, facebook callbacks) to record gameplay
--------------------------------------------------------------------------------


local Recorder = {}

-- listener types
Recorder.INPUT = "input"
Recorder.SINGLETON = "singleton"
Recorder.INSTANCE = "instance"

-- state
Recorder.IDLE = "idle"
Recorder.LOG = "log"
Recorder.RUN = "run"

--------------------------------------------------------------------------------
-- Public API
--------------------------------------------------------------------------------
function Recorder:init()
    self.state = Recorder.IDLE
    
    self.listeners = {}
    self.sensorCallbacks = {}
    
    self:overrideInputSensors()

    -- if MOAIFacebook then
    --     self:overrideGlobalListener("MOAIFacebook")

    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.DIALOG)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.SESSION_DID_LOGIN)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.SESSION_DID_NOT_LOGIN)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.DIALOG_DID_COMPLETE)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.DIALOG_DID_NOT_COMPLETE)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.PERMISSIONS_GRANTED)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.PERMISSIONS_DENIED)
    --     self:overrideGlobalEvent("MOAIFacebook", MOAIFacebook.REQUEST_RESPONSE)
    -- end
end


function Recorder:start()
    -- override loop flags for fully deterministic fixed step
    MOAISim.clearLoopFlags()
    MOAISim.setLoopFlags(MOAISim.LOOP_FLAGS_FIXED)

    self.data = {}
    self.state = Recorder.LOG
    self.frame = 0

    local stepCounter = MOAICoroutine.new()
    stepCounter:run(function()
        while true do
            self.frame = self.frame + 1
            coroutine.yield()
        end
    end)
    self.stepCounter = stepCounter
end


function Recorder:stop()
    self.state = Recorder.IDLE

    if self.stepCounter then
        self.stepCounter:stop()
        self.stepCounter = nil
    end
end


function Recorder:save(fileName)
    -- for k, v in pairs(self.data) do
    --     print(k, v)
    -- end
    MOAISerializer.serializeToFile(fileName, self.data)
end


function Recorder:run(fileName)
    local result = require(fileName)
    
    if not result then
        return
    end

    self.state = Recorder.RUN
    local thread = MOAICoroutine.new()
    self.frame = 0
    thread:run(function()
        while true do
            local frameEvents = result[self.frame]
            if frameEvents then
                for i, event in ipairs(frameEvents) do
                    self:executeEvent(event)
                end
            end
            self.frame = self.frame + 1
            coroutine.yield()
        end
    end)
    self.runThread = thread
end


--------------------------------------------------------------------------------
-- Private
--------------------------------------------------------------------------------
function Recorder:overrideInputSensors()
    local sensors = {
        "pointer",
        "mouseLeft",
        "touch",
        "keyboard",
    }

    local logger = self
    for i, sensorName in ipairs(sensors) do
        local sensor = MOAIInputMgr.device[sensorName]
        if sensor then
            sensor.__setCallback = sensor.setCallback
            sensor.setCallback = function(sensor, func)
                self:setListener(Recorder.INPUT, sensorName, nil, func)
            end

            local function callback(...)
                local params = {...}
                if logger.state == Recorder.LOG then
                    logger:logEvent(Recorder.INPUT, sensorName, nil, params)
                end
                if logger.state ~= Recorder.RUN then
                    logger.sensorCallbacks[sensorName](...)
                end
            end
            sensor:__setCallback(callback)
        end
    end
end


function Recorder:overrideGlobalListener(moaiClassName)
    local moaiClass = _G[moaiClassName]

    if not moaiClass then
        return
    end

    moaiClass.__setListener = moaiClass.setListener
    moaiClass.setListener = function(event, listener)
        self:setListener(Recorder.SINGLETON, moaiClassName, event, listener)
    end
end


function Recorder:overrideGlobalEvent(moaiClassName, event)
    local moaiClass = _G[moaiClassName]

    local logger = self
    local function callback(...)
        local params = {...}
        if logger.state == Recorder.LOG then
            logger:logEvent(Recorder.SINGLETON, moaiClassName, event, params)
        end
        if logger.state ~= Recorder.RUN then
            logger.listeners[moaiClassName][event](...)
        end
    end

    moaiClass.__setListener(event, callback)
end


function Recorder:overrideHttpTask()

end


function Recorder:overrideDataBuffer()

end


function Recorder:setListener(kind, name, event, listener)
    if kind == Recorder.INPUT then
        self.sensorCallbacks[name] = listener
    elseif kind == Recorder.SINGLETON then
        self.listeners[name] = self.listeners[name] or {}
        self.listeners[name][event] = listener
    end
end


function Recorder:logEvent(kind, name, event, params)
    local currentFrame = self.frame
    
    local frameData = self.data[currentFrame] or {}
    self.data[currentFrame] = frameData

    local eventData = {
        kind = kind,
        name = name,
        event = event,
        params = params,
    }
    table.insert(frameData, eventData)
end


function Recorder:executeEvent(data)
    if data.kind == Recorder.INPUT then
        local callback = self.sensorCallbacks[data.name]
        if callback then
            callback(unpack(data.params))
        end
    elseif data.kind == Recorder.SINGLETON then
        local callback = self.listeners[data.name] and self.listeners[data.name][data.event]
        if callback then
            callback(unpack(data.params))
        end
    end
end


return Recorder