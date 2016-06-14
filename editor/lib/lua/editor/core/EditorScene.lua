
local InputEvent = require("input.InputEvent")
local Entity = require("entity.Entity")

---------------------------------------------------------------------------------
--
-- @type EditorScene
--
---------------------------------------------------------------------------------

local EditorScene = Class("EditorScene" ):FIELDS{
}

function EditorScene:init( option )
	option = option or {}
    
    self.renderTbl = {}
    self.layersByName = {}
    self.entities = {}

    local group = Entity()
    self.rootGroup = group

    self.defaultLayer = self:addLayer( "default" )
end

---------------------------------------------------------------------------------
function EditorScene:getRender()
	return self.renderTbl
end

---------------------------------------------------------------------------------
function EditorScene:setInputDevice( inputDevice )
    self.inputDevice = inputDevice
end

---------------------------------------------------------------------------------
function EditorScene:addLayer( name, addlayer, index )
    local name = name or string.format("layer%d", #self.renderTbl)

    local layer = self.layersByName[name]
    if not layer then
        local index = index or (1 + #self.renderTbl)
        index = math.clamp(index, 1, #self.renderTbl + 1)
        layer = addlayer or MOAILayer.new()
        table.insert(self.renderTbl, index, layer)
        self.layersByName[name] = layer
    end

    return layer
end

function EditorScene:getLayer( name )
    local name = name or "default"
    return self.layersByName[name]
end

---------------------------------------------------------------------------------
function EditorScene:getRootGroup()
    return self.rootGroup
end

function EditorScene:setRootGroup( group )
    if self.rootGroup then
        local root = self.rootGroup
        root:removeChildren()
        self.rootGroup = nil
    end

    self.rootGroup = group
end


---------------------------------------------------------------------------------
function EditorScene:addEntity( entity, layer )
    assert( entity )

    local layer = layer or entity.layer
    if layer then
        if type(layer) == "string" then
            local layerName = layer
            layer = self:getLayer( layerName )
        end

        if entity.layer then
            self:addLayer( nil, entity.layer )
        end
    end

    layer = layer or self:getLayer()

    assert( layer )
    entity:_insertToScene( self, layer )
    self.entities[entity] = true

    return entity
end

function EditorScene:removeEntity( entity )
    if entity then
        local parent = entity.parent
        if parent then
            parent:removeChild( entity )
        end

        if self.entities[entity] then
            self.entities[entity] = nil
            entity:_removeFromScene()
        end
    end
end

---------------------------------------------------------------------------------

return EditorScene
