function onLoad()
	local viewport = MOAIViewport.new ()
	viewport:setSize ( 400, 400 )
	viewport:setScale ( 400, 400 )

	local layer = MOAILayer2D.new ()
	layer:setViewport ( viewport )

	local gfxQuad = MOAIGfxQuad2D.new ()
	gfxQuad:setTexture ( editorAsset("moai.png") )
	gfxQuad:setRect ( -64, -64, 64, 64 )

	local prop = MOAIProp2D.new ()
	prop:setDeck ( gfxQuad )
	prop:setLoc ( 0, 0 )

	layer:insertProp ( prop )

	local framebuffer = MOAIFrameBuffer.new()
	framebuffer:setClearColor( 0.5, 0.5, 0.5, 1 )
	framebuffer:setRenderTable( { layer } )

	if editor and editor.contextMgr then
		editor.contextMgr:updateCurrentContext( { framebuffer } )
	end

	print("Loaded LayoutView")
end