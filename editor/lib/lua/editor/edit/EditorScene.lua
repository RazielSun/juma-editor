
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

    self.viewport = option.viewport or App.viewport
    self:initLayers()

    local group = Entity()
    self.rootGroup = group
end

---------------------------------------------------------------------------------
function EditorScene:getRender()
	return self.renderTbl
end

function EditorScene:initLayers()
    self.defaultLayer = self:addLayer( "default" )
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
        
        if type(layer) == 'table' then
            for _, l in ipairs(layer) do
                self:setViewport( l )
            end
        else
            self:setViewport( layer )
        end
    end
    return layer
end

function EditorScene:setViewport( layer )
    local viewport = layer:getViewport()
    layer:setViewport( viewport or self.viewport )
end

function EditorScene:getLayer( name )
    if not name then
        return self.defaultLayer
    end
    return self.layersByName[name]
end

function EditorScene:setCameraForLayers( layers, camera )
    assert( camera )
    for i, layer in ipairs(layers) do
        if type(layer) == "table" then
            self:setCameraForLayers( layer, camera )
        else
            layer:setCamera( camera )
        end
    end
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

    local layer = layer or entity.layer or self.defaultLayer
    if type(layer) == "string" then
        local layerName = layer
        layer = self:getLayer( layerName )
    end
    layer = layer or self.defaultLayer

    if layer ~= self.defaultLayer and entity.layer == layer then
        self:addLayer( nil, layer )
    end

    if entity.layers then
        for _, la in ipairs(entity.layers) do
            self:addLayer( nil, la )
        end
    end

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
