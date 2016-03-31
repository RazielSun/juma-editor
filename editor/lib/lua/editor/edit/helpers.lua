--------------------------------------------------------------------------------
--
--------------------------------------------------------------------------------

function takeScreenshot()
	print("Take screenshot ...")
	Executors.callOnce( function ()
	    local buffer = MOAIFrameBufferTexture.new()
	    local screenW, screenH = MOAIEnvironment.horizontalResolution, MOAIEnvironment.verticalResolution
	    buffer:init(screenW, screenH)

	    MOAIRenderMgr.setBufferTable({buffer})
	    buffer:setRenderTable(MOAIGfxDevice.getFrameBuffer():getRenderTable())
	    buffer:setClearColor(RenderMgr:getClearColor())
	    local img = MOAIImage.new()
	    buffer:grabNextFrame(img, function()
	        local w, h = img:getSize()
	        -- local locale = MOAIEnvironment.languageCode
	        img:writePNG(string.format("%d_%dx%d.png", os.time(), w, h))
	    end)
	    coroutine.yield()

	    MOAIRenderMgr.setBufferTable(nil)
	    buffer:setRenderTable(nil)
	end )
end

function garbageCollect()
	print("Garbage collect ...")
	MOAISim.forceGC()
end

--------------------------------------------------------------------------------
function _createNodeHelperForUI( entity )
	entity.updateNode = MOAIScriptNode.new()
	entity.updateNode:setCallback( function() entity:updateAnchor() end )
	entity.updateNode:setNodeLink( entity:getProp() )
end