local Entity = require("core.Entity")

function onLoad()
	local scene = EditorSceneMgr:setupScene()

	local entity = Entity()
	scene.root:addChild( entity )
end

function onResize( width, height )
	local scene = EditorSceneMgr:getScene()
	if scene then
		scene:resize( width, height )
	end
end