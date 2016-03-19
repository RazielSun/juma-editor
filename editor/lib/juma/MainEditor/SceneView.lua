function onLoad()
	local scene = EditorSceneMgr:setupScene()
end

function onResize( width, height )
	local scene = EditorSceneMgr:getScene()
	if scene then
		scene:resize( width, height )
	end
end