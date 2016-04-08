
local EditorEntity = require("edit.EditorEntity")
local TransformProxy = require("edit.tools.TransformProxy")

---------------------------------------------------------------------------------
--
-- @type TransformToolHelper
--
---------------------------------------------------------------------------------

local TransformToolHelper = Class( EditorEntity, "TransformToolHelper" )

_wrapWithMoaiPropMethods( TransformToolHelper, '_prop' )

function TransformToolHelper:init()
	EditorEntity.init(self)

	self._prop = MOAIProp.new()
	self._prop.entity = self
	
	self.updateNode = MOAIScriptNode.new()	
	self.syncing = false
	self.updateTranslation = true
	self.updateRotation    = true
	self.updateScale       = true
end

function TransformToolHelper:setUpdateMasks( translation, rotation, scale )
	self.updateTranslation = translation or false
	self.updateRotation    = rotation    or false
	self.updateScale       = scale       or false
end

function TransformToolHelper:getProp()
	return self._prop
end

---------------------------------------------------------------------------------
function TransformToolHelper:setTargets( targets )
	self.targets = targets
	local proxies = {}
	self.proxies = proxies

	local count = 0
	local prop  = self._prop
	for e in pairs( targets ) do		
		local proxy = TransformProxy()
		proxy:setTarget( e )
		proxies[ e ] = proxy
		proxy:attachToTransform( prop )
		count = count + 1
	end
	self.targetCount = count
	self:updatePivot()
	self:syncFromTarget()
	self.updateNode:setCallback( function() self:onUpdate() end )
	self.updateNode:setNodeLink( prop )
end

function TransformToolHelper:preTransform()
	self:syncFromTarget()
	self.rot0 = { self:getRot() }
	self.scl0 = { self:getScl() }
end

function TransformToolHelper:updatePivot()
	local totalX, totalY = 0, 0
	for entity in pairs( self.targets ) do
		entity:forceUpdate()
		local x1,y1 = entity:modelToWorld( entity:getPiv() )
		totalX = totalX + x1
		totalY = totalY + y1		
	end
	local count = self.targetCount
	self:setLoc( totalX/count, totalY/count, 0 )	

	local rotZ = 0
	if count == 1 then
		rotZ = next( self.targets ):getProp():getAttr( MOAITransform.ATTR_Z_ROT )
	end
	self:getProp():setAttr( MOAITransform.ATTR_Z_ROT, rotZ )
end

function TransformToolHelper:syncFromTarget()
	self.syncing = true
	self:forceUpdate()
	for entity, proxy in pairs( self.proxies ) do
		proxy:syncFromTarget()
	end
	self.syncing = false
end

function TransformToolHelper:onUpdate()
	if self.syncing then return end
	self.syncing = true
	self:forceUpdate()
	local rx0, ry0, rz0 = unpack( self.rot0 )
	local sx0, sy0, sz0 = unpack( self.scl0 )
	local sx1, sy1, sz1 = self:getScl()
	local rx1, ry1, rz1 = self:getRot()
	local ssx, ssy, ssz = 0, 0, 0
	if sx1 ~= 0 then ssx = sx1/sx0 end
	if sy1 ~= 0 then ssy = sy1/sy0 end
	if sz1 ~= 0 then ssz = sz1/sz0 end
	local drx, dry, drz = rx1 - rx0, ry1 - ry0, rz1 - rz0
	local updateTranslation = self.updateTranslation
	local updateRotation = self.updateRotation
	local updateScale = self.updateScale
	for entity, proxy in pairs( self.proxies ) do
		proxy:syncToTarget(
			drx, dry, drz, ssx ,ssy, ssz, 
			updateTranslation, updateRotation, updateScale
		)
		emitPythonSignal( 'entity.modified', entity )
	end
	self.syncing = false
end

---------------------------------------------------------------------------------

return TransformToolHelper
