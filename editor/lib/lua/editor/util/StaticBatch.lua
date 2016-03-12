--------------------------------------------------------------------------------
-- StaticBatch.lua
-- 
-- 
-- Batch quads from MOAIGfxQuadDeck2D into single VBO mesh. Use for scenery that is mostly static. 
--------------------------------------------------------------------------------

local StaticBatch = class()

-- in quads
StaticBatch.DEFAULT_CAPACITY = 16

-- In bytes. Format is XYZWUVC, 16 + 8 + 4
local VTX_SIZE = 28

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:addQuad(deck, idx, transform)
    self:affirmCapacity()

    self.quad:setQuad(1, deck:getQuad(idx))
    self.quad:setUVQuad(1, deck:getUVQuad(idx))
    self.quad:transform(transform)

    self:writeQuad(self.count - 1)
    return self.count - 1
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:affirmCapacity(n)
    n = n or 1
    if self.count + n > self.capacity then
        self.capacity = math.floor(math.max(self.count + n, 1.5 * self.capacity))
        self:reserve()
    end
    self.count = self.count + n
    self.mesh:setTotalElements(6 * self.count)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:bless()
    self.vtxBuf:bless()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:fillIndices()
    local buf = self.idxBuf
    for i = 0, self.capacity - 1 do
        buf:setIndex(i * 6 + 1, i * 4 + 1 ) -- left top
        buf:setIndex(i * 6 + 2, i * 4 + 4 ) -- left bottom
        buf:setIndex(i * 6 + 3, i * 4 + 3 ) -- right bottom
        
        buf:setIndex(i * 6 + 4, i * 4 + 1 ) -- left top
        buf:setIndex(i * 6 + 5, i * 4 + 3 ) -- right bottom
        buf:setIndex(i * 6 + 6, i * 4 + 2 ) -- right top
    end
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:init(capacity)
    self.quad = MOAIGfxQuadDeck2D.new()
    self.quad:reserve(1)

    local prop = MOAIProp.new()

    local mesh = MOAIMesh.new()
    local idxBuf = MOAIIndexBuffer.new()
    local vtxBuf = MOAIVertexBuffer.new()

    local format = MOAIVertexFormatMgr.getFormat(MOAIVertexFormatMgr.XYZWUVC)
    vtxBuf:setFormat(format)
    vtxBuf:reserveVBOs(1)

    prop:setDeck(mesh)
    mesh:setIndexBuffer(idxBuf)
    mesh:setVertexBuffer(vtxBuf)

    self.prop = prop
    self.mesh = mesh
    self.idxBuf = idxBuf
    self.vtxBuf = vtxBuf

    self.capacity = capacity or StaticBatch.DEFAULT_CAPACITY
    self.count = 0
    self:reserve()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:reserve()
    self.vtxBuf:reserveVerts(4 * self.capacity)
    self.idxBuf:reserve(6 * self.capacity)

    self:fillIndices()
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:replaceQuad(index, deck, idx, transform)
    self.quad:setQuad(deck:getQuad(idx))
    self.quad:setUVQuad(deck:getUVQuad(idx))
    self.quad:transform(transform)

    self:writeQuad(index)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:removeQuad(index)
    if index >= self.count then return end

    local buf = self.vtxBuf
    local s = VTX_SIZE * 4
    buf:seek(s * (index + 1))
    local data = buf:read(s * (self.capacity - index - 1))
    buf:seek(s * index)
    buf:write(data)

    self.count = self.count - 1
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:setTexture(texture)
    self.mesh:setTexture(texture)
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function StaticBatch:writeQuad(index)
    self.vtxBuf:seek(4 * VTX_SIZE * index)
    self.quad:copyToVtxBuffer(self.vtxBuf, 1)
end


return StaticBatch
