--------------------------------------------------------------------------------
-- Mesh primitives for drawing
-- 
-- 
--------------------------------------------------------------------------------

local MeshPrimitives = {}

---
-- Utility class for mesh primitives
-- 

local function writeVec(buf, x, y, z)
    buf:writeFloat(x)
    buf:writeFloat(y)
    buf:writeFloat(z)
end

---
-- Return MOAIMesh deck initialized with colored rectangle (color here is value for vertex attributes)
function MeshPrimitives:rect(width, height, color)
    assert(width)
    assert(height)
    color = color or {1, 1, 1, 1}

    local mesh = MOAIMesh.new()

    local vertexBuf = MOAIVertexBuffer.new()
    local indexBuf = MOAIIndexBuffer.new()

    local vertexFormat = MOAIVertexFormat.new()
    vertexFormat:declareCoord( 1, MOAIVertexFormat.GL_FLOAT, 3)
    vertexFormat:declareColor( 2, MOAIVertexFormat.GL_UNSIGNED_BYTE)

    local x1, x2 = -0.5 * width, 0.5 * width
    local y1, y2 = -0.5 * heigth, 0.5 * height

    vertexBuf:setFormat(vertexFormat)
    vertexBuf:reserveVerts(4)

    writeVec(vertexBuf, x1, y2, 0)
    vertexBuf:writeColor32(unpack(color))
    writeVec(vertexBuf, x1, y1, 0)
    vertexBuf:writeColor32(unpack(color))
    writeVec(vertexBuf, x2, y1, 0)
    vertexBuf:writeColor32(unpack(color))
    writeVec(vertexBuf, x2, y2, 0)
    vertexBuf:writeColor32(unpack(color))

    indexBuf:reserve(6)
    indexBuf:setIndex(1, 1)
    indexBuf:setIndex(2, 2)
    indexBuf:setIndex(3, 3)
    indexBuf:setIndex(4, 3)
    indexBuf:setIndex(5, 4)
    indexBuf:setIndex(6, 1)

    mesh:setIndexBuffer(indexBuf)
    mesh:setVertexBuffer(vertexBuf)
    mesh:setPrimType(MOAIMesh.GL_TRIANGLES)

    return mesh
end


---
-- 




return MeshPrimitives