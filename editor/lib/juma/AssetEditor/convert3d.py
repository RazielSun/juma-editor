import pyassimp
import pyassimp.postprocess

luaAdd = """
function(data, out)
    local vtxFormat = MOAIVertexFormat.new()
    vtxFormat:declareCoord ( 1, MOAIVertexFormat.GL_FLOAT, 3 )
    vtxFormat:declareUV ( 2, MOAIVertexFormat.GL_FLOAT, 2 )
    vtxFormat:declareColor ( 3, MOAIVertexFormat.GL_UNSIGNED_BYTE )

    local vtxCount = data.verticesCount
    local idxCount = 3 * data.facesCount

    local vtxBuffer = MOAIVertexBuffer.new ()
    local idxBuffer = MOAIIndexBuffer.new ()
    vtxBuffer:reserve ( vtxCount * vtxFormat:getVertexSize ())

    idxBuffer:setIndexSize ( 4 )
    idxBuffer:reserve ( idxCount * 4 )

    local bakeLightFromNormals = true
    local ambient = {0.7, 0.7, 0.7}
    local diffuse = 0.3
    local light = {0.14, 0.98, 0.14}
    local function luminosity(r, g, b)
        return light[1] * r + light[2] * g + light[3] * b
    end

    for i = 0, vtxCount - 1 do
        -- TODO: vertex colors, multiple UV channels
        local vtx = data.vertices [ i ]
        local uv = data.texturecoords [ 0 ][ i ]
        vtxBuffer:writeFloat ( vtx [ 0 ], vtx [ 1 ], vtx [ 2 ])
        vtxBuffer:writeFloat ( uv [ 0 ], uv [ 1 ])

        if bakeLightFromNormals then
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

    out [ data.name ] = mesh
end
"""

luaSerialize = """
function(tbl, path)
    MOAISerializer.serializeToFile(path, tbl)
end
"""

def recur_node(node,level = 0):
    print("  " + "\t" * level + "- " + str(node))
    for child in node.children:
        recur_node(child, level + 1)

def convert3dScene(inPath, outPath, lua):
    outTable = lua.eval('{}')
    add = lua.eval(luaAdd)
    serialize = lua.eval(luaSerialize)

    scene = pyassimp.load(inPath, None, 
        pyassimp.postprocess.aiProcess_ImproveCacheLocality | 
        pyassimp.postprocess.aiProcess_Triangulate | 
        pyassimp.postprocess.aiProcess_FlipUVs
    )
    
    #the model we load
    print("MODEL:" + inPath)
    print
    
    #write some statistics
    print("SCENE:")
    print("  meshes:" + str(len(scene.meshes)))
    print("  materials:" + str(len(scene.materials)))
    print("  textures:" + str(len(scene.textures)))
    print
    
    print("NODES:")
    recur_node(scene.rootnode)

    print
    print("MESHES:")
    for index, mesh in enumerate(scene.meshes):
        print("  MESH id: " + str(index+1) + " (" + str(mesh.name) + ")")
        print("    material id: " + str(mesh.materialindex+1))
        print("    vertices: " + str(len(mesh.vertices)))
        print("    normals: " + str(len(mesh.normals)))
        print("    colors: " + str(len(mesh.colors)))
        print("    uv channels: " + str(len(mesh.texturecoords)))
        print("    uv-component-count:" + str(len(mesh.numuvcomponents)))
        print("    faces:" + str(len(mesh.faces)))
        print("    bones:" + str(len(mesh.bones)))
        print
        meshDict = {
            'name'          : mesh.name or index,
            'vertices'      : mesh.vertices,
            'verticesCount' : len(mesh.vertices),
            'texturecoords' : mesh.texturecoords,
            'faces'         : mesh.faces,
            'facesCount'    : len(mesh.faces),
            'bones'         : mesh.bones,
            'normals'       : mesh.normals
        }
        add(meshDict, outTable, index)

    print("MATERIALS:")
    for index, material in enumerate(scene.materials):
        print("  MATERIAL (id:" + str(index+1) + ")")
        for key, value in material.properties.items():
            print("    %s: %s" % (key, value))
    print
    
    print("TEXTURES:")
    for index, texture in enumerate(scene.textures):
        print("  TEXTURE" + str(index+1))
        print("    width:" + str(texture.width))
        print("    height:" + str(texture.height))
        print("    hint:" + str(texture.achformathint))
        print("    data (size):" + str(len(texture.data)))
    
    serialize(outTable, outPath)

    # Finally release the model
    pyassimp.release(scene)

    # def showAssimpFileDialog(self):
    #     fileName, filt = QtGui.QFileDialog.getOpenFileName(self, "3d scene (model)", self.workingDir or "~")
    #     if fileName:
    #         outPath = os.path.splitext(fileName)[0] + '.lua'
    #         convert3dScene(fileName, outPath, self.moaiWidget.lua)