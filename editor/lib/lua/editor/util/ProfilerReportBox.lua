--------------------------------------------------------------------------------
-- ProfilerReportBox.lua
-- 
-- Renders current profiler stats
--------------------------------------------------------------------------------

local RenderMgr = require("core.RenderMgr")
local Layer = require("core.Layer")
local Label = require("core.Label")

local ProfilerReportBox = class()

local alpha = 0.02
local MAX_VALUES = 120

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:init()
    self.frameRate      = 0
    self.drawCalls      = 0
    self.objectCount    = 0
    self.luaMemory      = 0
    self.textureMemory  = 0
    self.luagc          = 0
    self.renderTime     = 0
    self.simTime        = 0
    self.actionMgr      = 0
    self.nodeMgr        = 0

    self.layer = Layer()

    self.rawSim = {}
    self.rawRender = {}
    self.rawDt = {}
    self.head = 1
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:initBox(font)
    self.textBox = Label("", nil, nil, font, 8, false)
    self.textBox:setAlignment(MOAITextBox.RIGHT_JUSTIFY, MOAITextBox.TOP_JUSTIFY)
    self.textBox:setColor(1, 1, 1, 1)

    local image = MOAIImage.new()
    image:init(16, 16)
    image:fillRect(0, 0, 16, 16, 0, 0, 0, 0.6)
    local tex = MOAITexture.new()
    tex:load(image)

    local bgDeck = MOAIGfxQuad2D.new()
    bgDeck:setRect(-0.5, -0.5, 0.5, 0.5)
    bgDeck:setTexture(tex)

    local bg = MOAIProp.new()
    bg:setDeck(bgDeck)
    bg:setAttrLink(MOAITransform.INHERIT_TRANSFORM, self.textBox, MOAITransform.TRANSFORM_TRAIT)
    self.bg = bg

    bg:setLayer(self.layer)
    self.textBox:setLayer(self.layer)    
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:initPlot()
    local plotProp = MOAIProp.new()
    local plotDeck = MOAIScriptDeck.new()

    plotDeck:setDrawCallback(function() self:plot() end)
    plotDeck:setRect(-0.5 * App.viewWidth, -0.5 * App.viewHeight, 0.5 * App.viewWidth, 0.5 * App.viewHeight)

    plotProp:setDeck(plotDeck)
    plotProp:setLayer(self.layer)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:start()
    RenderMgr:addChild(self.layer)
    self.updateThread = MOAICoroutine.new()

    self.updateThread:run(function()
        local dt = MOAISim.getStep()
        while true do
            self:collectValues(dt)
            dt = coroutine.yield()
        end
    end)

    if self.textBox then
        self.renderThread = MOAICoroutine.new()
        self.renderThread:run(function()
            while true do
                self:render()
                coroutine.wait(0.5)
            end
        end)

        self.textBox:setLoc(0.5 * App.viewWidth - 6, 0.5 * App.viewHeight - 6)
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:stop()
    RenderMgr:removeChild(self.layer)
    
    if self.updateThread then
        self.updateThread:stop()
        self.updateThread = nil
    end

    if self.renderThread then
        self.renderThread:stop()
        self.renderThread = nil
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:collectValues(dt)
    local mem = MOAISim.getMemoryUsage()
    local objCount = MOAISim.getLuaObjectCount()
    local drawCalls = MOAIRenderMgr.getPerformanceDrawCount()
    local fr, am, nm, sd, rd = MOAISim.getPerformance()

    self.frameRate      = fr
    self.drawCalls      = drawCalls
    self.objectCount    = objCount
    self.luaMemory      = mem.lua
    self.textureMemory  = mem.texture
    self.luagc          = mem._luagc_count
    self.renderTime     = (1 - alpha) * self.renderTime + alpha * rd
    self.simTime        = (1 - alpha) * self.simTime + alpha * sd
    self.actionMgr      = (1 - alpha) * self.actionMgr + alpha * am
    self.nodeMgr        = (1 - alpha) * self.nodeMgr + alpha * nm

    self.rawSim[self.head] = sd
    self.rawRender[self.head] = rd
    self.rawDt[self.head] = dt
    self.head = self.head + 1
    if self.head > MAX_VALUES then self.head = 1 end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function ProfilerReportBox:render()
    local str = string.format([=[
FPS              %12.1f
Draw calls       %12d
Lua count        %12d
Lua memory       %12d
luagc_count      %12d
Texture memory   %12d
Render Time      %12.2f
Sim Time         %12.2f
ActionTree time  %12.2f
NodeMgr time     %12.2f]=], 
        self.frameRate, self.drawCalls, self.objectCount, self.luaMemory, self.luagc, 
        self.textureMemory, self.renderTime * 1000, self.simTime * 1000, self.actionMgr * 1000, self.nodeMgr * 1000)

    self.textBox:setString(str)
    local xMin, yMin, _, xMax, yMax = self.textBox:getBounds()
    self.bg:setScl(12 + xMax - xMin, 12 + yMax - yMin)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
local points = {}
function ProfilerReportBox:plot()
    local sim = self.rawSim
    local render = self.rawRender
    local delta = self.rawDt
    local count = #sim
    local head = math.min(self.head, count)
    local dt = 1/60

    local x0 = -0.5 * App.viewWidth
    local y0 = 0.5 * App.viewHeight - 100
    local step = (App.viewWidth - 100) / MAX_VALUES

    MOAIGfxDevice.setPenColor(0, 0, 0, 0.6)    
    MOAIDraw.fillRect(x0, y0, 0.5 * App.viewWidth - 100, 0.5 * App.viewHeight)

    for i = 0, count-1 do
        local y = 1 + (head - 1 + i) % count

        points[i * 2 + 1] = x0 + i * step
        points[i * 2 + 2] = y0 + sim[y] / dt * 30
    end
    MOAIGfxDevice.setPenColor(0, 0, 1, 1)
    MOAIDraw.drawLine(points)

    for i = 0, count-1 do
        local y = 1 + (head - 1 + i) % count

        points[i*2 + 1] = x0 + i * step
        points[i*2 + 2] = y0 + render[y] / dt * 30
    end
    MOAIGfxDevice.setPenColor(0, 1, 0, 1)
    MOAIDraw.drawLine(points)

    for i = 0, count-1 do
        local y = 1 + (head - 1 + i) % count

        points[i*2 + 1] = x0 + i * step
        points[i*2 + 2] = y0 + delta[y] / dt * 30
    end
    MOAIGfxDevice.setPenColor(1, 1, 0, 1)
    MOAIDraw.drawLine(points)

    MOAIGfxDevice.setPenColor(1, 0, 0, 1)
    MOAIDraw.drawLine(x0, y0 + 30, 0.5 * App.viewWidth - 100, y0 + 30)
end


return ProfilerReportBox
