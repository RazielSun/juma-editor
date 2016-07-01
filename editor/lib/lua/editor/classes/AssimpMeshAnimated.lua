function(data, out, bakeLight)
    local vtxFormat = MOAIVertexFormat.new()
    vtxFormat:declareCoord      ( 1, MOAIVertexFormat.GL_FLOAT, 3 )
    vtxFormat:declareUV         ( 2, MOAIVertexFormat.GL_FLOAT, 2 )
    -- bone weight[4]
    vtxFormat:declareAttribute  ( 3, MOAIVertexFormat.GL_FLOAT, 4, false, MOAIVertexFormat.VERTEX_USE_TUPLE )
    -- bone index[4]
    vtxFormat:declareAttribute  ( 4, MOAIVertexFormat.GL_FLOAT, 4, false, MOAIVertexFormat.VERTEX_USE_TUPLE )
    vtxFormat:declareColor      ( 5, MOAIVertexFormat.GL_UNSIGNED_BYTE )

    local vtxCount = data.verticesCount
    local idxCount = 3 * data.facesCount

    local vtxBuffer = MOAIVertexBuffer.new ()
    local idxBuffer = MOAIIndexBuffer.new ()
    vtxBuffer:reserve ( vtxCount * vtxFormat:getVertexSize ())

    idxBuffer:setIndexSize ( 4 )
    idxBuffer:reserve ( idxCount * 4 )

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    -- TODO: set those from UI    
    -- ambient light color
    local ambient = { 0.7, 0.7, 0.7 }

    -- light direction vector (normalized)
    local light = { 0.14, 0.98, 0.14 }

    -- diffuse power
    local diffuse = 0.3
    local function luminosity ( r, g, b )
        return light [ 1 ] * r + light [ 2 ] * g + light [ 3 ] * b
    end
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

    local function normalizeVec4(x, y, z, w)
        local r = math.sqrt(x * x + y * y + z * z + w * w)
        if r > 0 then
            local div = 1 / r
            return x * div, y * div, z * div, w * div
        end
        return 0, 0, 0, 1
    end

    -- populate per vertex weight and bone index arrays
    local boneCount = data.bonesCount
    local weights = {}
    for i = 0, boneCount - 1 do
        local bone = python.as_attrgetter ( data.bones [ i ])

        for vtxW in python.iter ( bone.weights ) do
            local vtxId = vtxW.vertexid
            if vtxW.weight > 0 then
                if not weights [ vtxId ] then weights [ vtxId ] = {} end
                table.insert ( weights [ vtxId ], { w = vtxW.weight, bone = i } )
            end
        end
    end

    -- sort weights, fill 0 to missing ones
    for _, w in pairs ( weights ) do
        table.sort ( w, function ( w1, w2 ) return w1.w > w2.w end)
        for i = 1, 4 do
            if not w [ i ] then
                w [ i ] = {w = 0, bone = 0}
            end
        end
    end


    for i = 0, vtxCount - 1 do
        local vtx = data.vertices [ i ]
        local uv = data.texturecoords [ 0 ][ i ]
        local w = weights [ i ]
        vtxBuffer:writeFloat ( vtx [ 0 ], vtx [ 1 ], vtx [ 2 ])
        vtxBuffer:writeFloat ( uv [ 0 ], uv [ 1 ])
        vtxBuffer:writeFloat ( w [ 1 ].w, w [ 2 ].w, w [ 3 ].w, w [ 4 ].w )
        vtxBuffer:writeFloat ( w [ 1 ].bone, w [ 2 ].bone, w [ 3 ].bone, w [ 4 ].bone )

        if bakeLight then
            local n = data.normals [ i ]
            local luma = math.max(0, luminosity ( n [ 0 ], n [ 1 ], n [ 2 ]))
            local r = math.min ( 1, ambient [ 1 ] + diffuse * luma )
            local g = math.min ( 1, ambient [ 2 ] + diffuse * luma )
            local b = math.min ( 1, ambient [ 3 ] + diffuse * luma )
            -- vtxBuffer:writeColor32 ( 0.5 + 0.5 * n [ 0 ], 0.5 + 0.5 * n [ 1 ], 0.5 + 0.5 * n [ 2 ], 1 )
            vtxBuffer:writeColor32 ( r, g, b, 1 )
        else
            vtxBuffer:writeColor32 ( 1, 1, 1, 1 )
        end
    end

    for face in python.iter ( data.faces ) do
        idxBuffer:writeU32 ( face [ 0 ], face [ 1 ], face [ 2 ])
    end

    local mesh = MOAIMesh.new ()
    mesh:setVertexBuffer ( vtxBuffer, vtxFormat )
    mesh:setIndexBuffer ( idxBuffer )

    mesh:setTotalElements ( idxCount )
    mesh:setBounds ( vtxBuffer:computeBounds ( vtxFormat ))

    mesh:setPrimType ( MOAIMesh.GL_TRIANGLES )

    if not out.meshes then out.meshes = {} end
    out.meshes [ data.name ] = mesh
end