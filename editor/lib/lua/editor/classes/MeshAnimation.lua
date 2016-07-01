

local CURVE_KINDS = {
    locX = MOAITransform.ATTR_X_LOC,
    locY = MOAITransform.ATTR_Y_LOC,
    locZ = MOAITransform.ATTR_Z_LOC,

    rotX = MOAITransform.ATTR_X_ROT,
    rotY = MOAITransform.ATTR_Y_ROT,
    rotZ = MOAITransform.ATTR_Z_ROT,

    sclX = MOAITransform.ATTR_X_SCL,
    sclY = MOAITransform.ATTR_Y_SCL,
    sclZ = MOAITransform.ATTR_Z_SCL,
}

---------------------------------------------------------------------------------
--
-- @type MeshAnimation
--
---------------------------------------------------------------------------------

local MeshAnimation = Class("MeshAnimation")

function MeshAnimation:init( option )
    self:setPath( option )
end

function MeshAnimation:reset()
    self.bones = {}
    self.transforms = {}
    self.boneNameMap = {}
end

---------------------------------------------------------------------------------
function MeshAnimation:setPath( path )
    local data = MOAIJsonParser.decode(MOAIFileSystem.loadFile(path))
    self:setAnimData( data )
end

function MeshAnimation:setAnimData( data )
    if not data then return end

    local animName, animData = next(data.animations)
    local animatedNodes = animData and animData.bones or {}
    
    self:reset()
    self:createNode(data.bones[1])

    local skeleton = MOAIBoneArray.new()
    skeleton:reserve(#self.bones)
    for i, bone in pairs(self.bones) do
        skeleton:setBone(i, bone)
    end
    self.skeleton = skeleton
    
    local program = MOAIShaderMgr.getProgram(MOAIShaderMgr.SKINNED_MESH_SHADER)
    local shader = MOAIShader.new()
    shader:setProgram(program)
    shader:setAttrLink(3, skeleton, MOAIBoneArray.ATTR_VEC4_ARRAY)
    self.shader = shader

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    local anim = MOAIAnim.new()
    anim:reserveLinks(self:countCurves(animatedNodes))
    self.anim = anim

    local idx = 1
    print(animatedNodes)
    for nodeName, curves in pairs(animatedNodes) do
        for kind, keys in pairs(curves) do
            if #keys > 0 then
                local node = self.boneNameMap[nodeName]
                self:makeCurve(kind, keys, anim, node, idx)
                idx = idx + 1
            end
        end
    end
    anim:setSpeed(animData.frameRate)
    anim:setSpan(animData.frames)
    anim:start()
    anim:setMode(MOAITimer.LOOP)
end

function MeshAnimation:createNode(node)
    local m = node.inverseBindPose
    local bone = MOAIBone.new()
    bone:setInvBindPose(
        m[1][1], m[1][2], m[1][3], m[1][4],
        m[2][1], m[2][2], m[2][3], m[2][4],
        m[3][1], m[3][2], m[3][3], m[3][4]
    )

    bone:setScl(unpack(node.scale))
    bone:setPreRotation(unpack(node.rotation))
    bone:setLoc(unpack(node.position))

    table.insert(self.bones, bone)

    for _, nd in pairs(node.children) do
        local child = self:createNode(nd)
        child:setAttrLink(MOAITransform.INHERIT_TRANSFORM, bone, MOAITransform.TRANSFORM_TRAIT)
    end
    self.boneNameMap[node.name] = bone
    return bone
end

---------------------------------------------------------------------------------
function MeshAnimation:makeCurve( kind, keys, anim, node, idx )
    local curve = MOAIAnimCurve.new()
    curve:reserveKeys(#keys)
    for i, key in pairs(keys) do
        curve:setKey(i, key.frame, key.value, MOAIEaseType.LINEAR)
    end
    self.anim:setLink(idx, curve, node, CURVE_KINDS[kind])
end


function MeshAnimation:countCurves( data )
    local count = 0
    for nodeName, curves in pairs(data) do
        for kind, keys in pairs(curves) do
            if #keys > 0 then
                count = count + 1
            end
        end
    end
    return count
end

---------------------------------------------------------------------------------

return MeshAnimation
