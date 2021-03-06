--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

local ParticleForce = require("ParticleForce")
local ParticleComponent = require("ParticleComponent")
local ParticleHelper = require("util.ParticleHelper")

local ParticleState = class()
ParticleState.__className = "ParticleState"

local DATA = {
    { type = "string", name = "Name", value = "state", access = "Name" },
    { type = "float", name = "Damping", value = 0, access = "Damping", range = {min = 0} },
    { type = "float", name = "Mass min", value = 1, access = "MassMin", range = {min = 0} },
    { type = "float", name = "Mass max", value = 1, access = "MassMax", range = {min = 0} },
    { type = "float", name = "Lifetime min", value = 1, access = "TermMin", range = {min = 0} },
    { type = "float", name = "Lifetime max", value = 1, access = "TermMax", range = {min = 0} },
    { type = "list",  name = "Next", value = 0, access = "Next", choices = {} },
    { type = "bool",  name = "User script", value = 0, access = "UserScript" },
}

local counter = 1

function ParticleState:addComponent(kind)
    if kind == 'Force' then
        self:addForce()
        return
    end

    local clazz = ParticleComponent[kind]
    if not clazz then
        log.error("Particle component not found " .. kind)
        return
    end

    local comp = clazz()
    table.insert(self.components, comp)
    self:syncComponents()
end

function ParticleState:addForce()
    local force = ParticleForce()
    table.insert(self.forces, force)
    self:syncForces()
end

function ParticleState:assignUniqueIds(data, prefix)
    local items = data.items
    if not items then return data end

    for i, info in pairs(items) do
        info.id = prefix .. "$" .. info.id
    end
    return data
end

function ParticleState:copyFrom(state)
    self:destroy()

    for _, default in ipairs(DATA) do
        local getter = 'get' .. default.access
        local setter = 'set' .. default.access
        self[setter](self, state[getter](state))
    end

    local name, num = string.match(state:getName(),  "^(.+)[%s]copy%s?(%d?)$")
    if not name then
        name = state:getName() .. " copy"
    else
        num = tonumber(num) or 0
        name = string.format("%s copy %d", name, num + 1)
    end
    self:setName(name)

    for _, force in pairs(state.forces) do
        local myForce = ParticleForce()
        myForce:copyFrom(force)
        table.insert(self.forces, myForce)
    end

    for _, comp in pairs(state.components) do
        local myComp = comp.__class()
        myComp:copyFrom(comp)
        table.insert(self.components, myComp)
    end

    self:syncForces()
    self:syncComponents()
end

function ParticleState:getModelData()
    local stateParams = {}
    for _, p in ipairs(DATA) do
        local getter = 'get' .. p.access
        local value = self[getter](self)

        local item = {
            type = p.type,
            name = p.name,
            id = p.access,
            value = value,
            range = p.range,
        }

        if p.access == "Next" then
            item.choices = require('ParticleEditor').listStates()
            table.insert(item.choices, 1, "None")
        end

        table.insert(stateParams, item)
    end

    local data = {
        { group = self:getName(), items = stateParams }
    }

    if #self.forces > 0 then
        for i, f in ipairs(self.forces) do
            local grp = self:assignUniqueIds(f:getGroupData(), 'force' .. i)
            table.insert(data, grp)
        end
    end

    if #self.components > 0 then
        for i, c in ipairs(self.components) do
            local grp = self:assignUniqueIds(c:getGroupData(), 'comp' .. i)
            table.insert(data, grp)
        end
    end

    return data
end

function ParticleState:getInitScript()
    return self.initScript
end

function ParticleState:getRenderScript()
    return self.renderScript
end

function ParticleState:getUserInitScript()
    return self.userInitScript or ''
end

function ParticleState:getUserRenderScript()
    return self.userRenderScript or ''
end

function ParticleState:getParam(paramId)
    local getter = self['get' .. paramId]
    if not getter then
        log.error("No getter for " .. paramId)
        return
    end

    return getter(self)
end

function ParticleState:getRegisterCount()
    if self.userScript ~= 0 then
        return self.registerCount or 0
    end

    local regCount = 0
    for _, comp in pairs(self.components) do
        regCount = regCount + comp:getRegisterCount()
    end
    return regCount
end

function ParticleState:init()
    self.state = MOAIParticleState.new()
    self.forces = {}
    self.components = {}
    self.mass = {0, 0}
    self.term = {0, 0}

    self.userInitScript = ""
    self.userRenderScript = ""

    for _, default in ipairs(DATA) do
        local setter = 'set' .. default.access
        self[setter](self, default.value)
    end

    self:setName("State" .. counter)
    counter = counter + 1

    self:syncComponents()
end


function ParticleState:destroy()
    for _, f in pairs(self.forces) do
        f:destroy()
    end

    for _, c in pairs(self.components) do
        c:destroy()
    end
    self.foces = {}
    self.components = {}
end

function ParticleState:hideGizmos()
    for _, force in pairs(self.forces) do
        force:hideGizmos()
    end
end

function ParticleState:removeComponent(paramId)
    local forceIdx = string.match(paramId, "force(%d+)%$(.*)")
    if forceIdx then
        local force = table.remove(self.forces, forceIdx)
        force:destroy()
        self:syncForces()
        return true
    end

    local compIdx = string.match(paramId, "comp(%d+)%$(.*)")
    if compIdx then
        local comp = table.remove(self.components, compIdx)
        comp:destroy()
        self:syncComponents()
        return true
    end
end

function ParticleState:serializeIn(serializer, data)
    for _, v in pairs(DATA) do
        self:setParam(v.access, data[v.access])
    end
    if data.nextState then
        self.next = serializer:getObjectById(data.nextState)
        self.state:setNext(self.next.state)
    end

    for _, forceId in pairs(data.forces) do
        local force = serializer:getObjectById(forceId)
        table.insert(self.forces, force)
    end

    for _, compId in pairs(data.components) do
        local comp = serializer:getObjectById(compId)
        table.insert(self.components, comp)
    end

    self:setUserInitScript(data.initScript or '')
    self:setUserRenderScript(data.renderScript or '')
end

function ParticleState:serializeOut(serializer, out)
    for _, v in pairs(DATA) do
        out[v.access] = self:getParam(v.access)
    end
    if self.next then
        out.nextState = serializer:affirmObjectId(self.next)
    end

    out.forces = {}
    for _, force in pairs(self.forces) do
        table.insert(out.forces, serializer:affirmObjectId(force))
    end

    out.components = {}
    for _, comp in pairs(self.components) do
        table.insert(out.components, serializer:affirmObjectId(comp))
    end

    out.initScript = self:getUserInitScript()
    out.renderScript = self:getUserRenderScript()
end

function ParticleState:setForceParam(paramId, value)
    local idx, param = string.match(paramId, "force(%d+)%$(.*)")
    if idx and param then
        local force = self.forces[tonumber(idx)]
        if force then
            return force:setParam(param, value)
        end
    end
end

function ParticleState:setComponentParam(paramId, value)
    local idx, param = string.match(paramId, "comp(%d+)%$(.*)")
    if idx and param then
        local comp = self.components[tonumber(idx)]
        if comp then
            local res = comp:setParam(param, value)
            self:syncComponents()
            return res
        end
    end
end

function ParticleState:setUserInitScript(script)
    self.userInitScript = script
    self:updateScripts()
end

function ParticleState:setUserRenderScript(script)
    self.userRenderScript = script
    self:updateScripts()
end

function ParticleState:setParam(paramId, value)
    if string.sub(paramId, 1, #'force') == 'force' then
        return self:setForceParam(paramId, value)
    end
    if string.sub(paramId, 1, #'comp') == 'comp' then
        return self:setComponentParam(paramId, value)
    end

    local setter = self['set' .. paramId]
    if not setter then
        log.error("No setter for " .. paramId)
        return
    end

    return setter(self, value)
end


function ParticleState:syncComponents()
    local init = {}
    local sim = {}
    local sprite = {}
    for _, comp in pairs(self.components) do
        table.insert(init, comp:getInitScript() or nil)
        table.insert(sim, comp:getSimScript() or nil)
        table.insert(sprite, comp:getSpriteScript() or nil)
    end

    self.initScript = table.concat(init, '\n')
    self.renderScript = table.concat(sim, '\n') .. '\nsprite()\n' .. table.concat(sprite, '\n')

    self:updateScripts()
end


function ParticleState:syncForces()
    self.state:clearForces()
    for _, f in ipairs(self.forces) do
        self.state:pushForce(f.force)
    end
end

function ParticleState:updateScripts()
    local initScript
    local renderScript

    if self.userScript == 0 then
        initScript = self.initScript
        renderScript = self.renderScript
    else
        initScript = self.userInitScript
        renderScript = self.userRenderScript
    end

    local initFunc, err = loadstring(initScript)
    if not initFunc then 
        log.error('Error loading init script: ', err)
        return
    end

    local renderFunc, err = loadstring(renderScript)
    if not renderFunc then
        log.error('Error loading render script: ', err)
        return
    end

    local reg = {}
    
    local res, init = pcall( ParticleHelper.makeParticleScript, initFunc, reg )
    if not res then
        log.error('Error compiling init script: ', init)
        return
    end
    local res, render = pcall( ParticleHelper.makeParticleScript, renderFunc, reg )
    if not res then
        log.error('Error compiling render script: ', render)
        return
    end
    log.info(init, render)

    self.state:setInitScript(init)
    self.state:setRenderScript(render)

    log.info(initScript)
    log.info(renderScript)
    log.info(table.pretty(reg))

    if self.userScript ~= 0 then
        local c = 0
        for k, v in pairs(reg.named) do
            c = c + 1
        end
        self.registerCount = c
    end

    require('ParticleEditor').updateRegCount()
end


--============================================================================--
-- Attribute accessors
--============================================================================--

function ParticleState:getDamping()
    return self.damping
end

function ParticleState:getMassMax()
    return self.mass[2]
end

function ParticleState:getMassMin()
    return self.mass[1]
end

function ParticleState:getName()
    return self.name
end

function ParticleState:getNext()
    if self.next then
        return require('ParticleEditor').getStateIdx(self.next)
    end
    return 0
end

function ParticleState:getTermMax()
    return self.term[2]
end

function ParticleState:getTermMin()
    return self.term[1]
end

function ParticleState:getUserScript()
    return self.userScript
end

function ParticleState:setDamping(damp)
    self.damping = damp
    self.state:setDamping(damp)
end

function ParticleState:setMassMax(mass)
    self.mass[2] = mass
    self.state:setMass(unpack(self.mass))
end

function ParticleState:setMassMin(mass)
    self.mass[1] = mass
    self.state:setMass(unpack(self.mass))
end

function ParticleState:setName(n)
    self.name = n
end

function ParticleState:setNext(idx)
    local st = require('ParticleEditor').findState(idx)
    self.next = st
    self.state:setNext(st and st.state)
end

function ParticleState:setTermMax(term)
    self.term[2] = term
    self.state:setTerm(unpack(self.term))
end

function ParticleState:setTermMin(term)
    self.term[1] = term
    self.state:setTerm(unpack(self.term))
end

function ParticleState:setUserScript(flag)
    self.userScript = flag
end


return ParticleState
