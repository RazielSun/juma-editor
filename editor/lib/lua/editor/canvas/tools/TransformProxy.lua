
---------------------------------------------------------------------------------
--
-- @type TransformProxy
--
---------------------------------------------------------------------------------

local TransformProxy = Class( "TransformProxy" )

function TransformProxy:init()
	self.proxy = MOAITransform.new()
end

---------------------------------------------------------------------------------
function TransformProxy:setTarget( target )
	self.target = target
end

function TransformProxy:attachToTransform( trans )
	self.proxy:setAttrLink ( MOAITransform.INHERIT_TRANSFORM, trans, MOAITransform.TRANSFORM_TRAIT )
end

function TransformProxy:syncFromTarget()
	local target, proxy = self.target, self.proxy
	target:forceUpdate()
	proxy:forceUpdate()
	self:onSyncFromTarget()
	proxy:forceUpdate()
end

function TransformProxy:syncToTarget( 
	drx, dry, drz, ssx ,ssy, ssz,
	updateTranslation, updateRotation, updateScale
	)

	local target, proxy = self.target, self.proxy
	target:forceUpdate()
	proxy:forceUpdate()
	self:onSyncToTarget( drx, dry, drz, ssx ,ssy, ssz )
	target:forceUpdate()
	-- if updateTranslation then
	-- 	mock.markProtoInstanceOverrided( target, 'loc' )
	-- end
	-- if updateRotation then
	-- 	mock.markProtoInstanceOverrided( target, 'rot' )
	-- end
	-- if updateScale then
	-- 	mock.markProtoInstanceOverrided( target, 'scl' )
	-- end
end

-- function markProtoInstanceOverrided( obj, fid )
-- 	if not obj.__proto_history then return false end
-- 	local overridedFields = obj.__overrided_fields
-- 	if not overridedFields then
-- 		overridedFields = {}
-- 		obj.__overrided_fields = overridedFields
-- 	end

-- 	if not overridedFields[ fid ] then
-- 		overridedFields[ fid ] = true
-- 		return true
-- 	end

-- 	return false
-- end

function TransformProxy:onSyncToTarget( drx, dry, drz, ssx ,ssy, ssz )
	local target, proxy = self.target, self.proxy
	CTHelper.setWorldLoc( target:getProp(), proxy:getWorldLoc() )
	-- target:getProp():setLoc( proxy:getLoc() ) WHy?
	local sx, sy, sz = proxy:getScl()
	local rx, ry, rz = proxy:getRot()
	target:setScl( sx*ssx, sy*ssy, sz*ssz )
	target:setRot( rx+drx, ry+dry, rz+drz )
end


function TransformProxy:onSyncFromTarget()
	local target, proxy = self.target, self.proxy
	CTHelper.setWorldLoc( proxy, target:modelToWorld( target:getPiv() ) )
	-- proxy:setLoc( target:modelToWorld( target:getPiv() ) ) WHy?
	proxy:setScl( target:getScl() )
	proxy:setRot( target:getRot() )
end
---------------------------------------------------------------------------------

return TransformProxy
