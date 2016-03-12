--------------------------------------------------------------------------------
--
--
--------------------------------------------------------------------------------

local ComboDeck = class()


function ComboDeck:create()
    local deck = MOAIGfxQuadListDeck2D.new()

    local quadIdx, pairIdx = 1, 1
    local quads = {}
    local knownSprites = {}
    local lists = {}
    local qPairs = {}
    local names = {}
    local atlasDeck

    for name, combo in pairs(self.params) do
        atlasDeck = atlasDeck or ResourceMgr:getDeck(combo[1])
        table.insert(lists, #combo)

        for i, sprite in pairs(combo) do
            if not knownSprites[sprite] then
                local idx = atlasDeck.names[sprite]
                quads[quadIdx] = {
                    quad = {atlasDeck:getQuad(idx)},
                    uv = {atlasDeck:getUVQuad(idx)}
                }

                knownSprites[sprite] = quadIdx
                quadIdx = quadIdx + 1
            end
            qPairs[pairIdx] = knownSprites[sprite]
            pairIdx = pairIdx + 1
            names[name] = #lists
        end
    end
    
    deck:reserveLists(#lists)
    deck:reservePairs(#qPairs)
    deck:reserveQuads(#quads)
    deck:reserveUVQuads(#quads)

    for i, quad in pairs(quads) do
        deck:setQuad(i, unpack(quad.quad))
        deck:setUVQuad(i, unpack(quad.uv))
    end

    for i, pair in pairs(qPairs) do
        deck:setPair(i, pair, pair)
    end

    local total = 1
    for i, run in pairs(lists) do
        deck:setList(i, total, run)
        total = total + run
    end

    deck:setTexture(atlasDeck.texture)
    deck.texture = atlasDeck.texture
    deck.names = names

    return deck
end

function ComboDeck:init(name, params)
    self.name = name
    self.params = params
end

function ComboDeck:key()
    return self.name
end

function ComboDeck:names()
    local list = {}
    for k, _ in pairs(self.params) do
        table.insert(list, k)
    end
    return list
end


return ComboDeck
