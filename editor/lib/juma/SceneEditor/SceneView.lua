function onLoad()
	local scene = EditorSceneMgr:setupScene()

	local gfxQuad = MOAIGfxQuad2D.new ()
	gfxQuad:setTexture ( editorAsset("moai.png") )
	gfxQuad:setRect ( -64, -64, 64, 64 )

	local prop = MOAIProp2D.new ()
	prop:setDeck ( gfxQuad )
	prop:setLoc ( 0, 0 )
	prop:setScl( 10, 10, 10 )

	scene.layer:insertProp ( prop )
end

function onResize( width, height )
	local scene = EditorSceneMgr:getScene()
	if scene then
		scene:resize( width, height )
	end
end