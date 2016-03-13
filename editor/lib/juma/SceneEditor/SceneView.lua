function onLoad()
	-- MOAISim.openWindow ( "test", 600, 400 )
	local viewport = MOAIViewport.new ()
	viewport:setSize ( 600, 400 )
	viewport:setScale ( 600, 400 )

	local layer = MOAILayer2D.new ()
	layer:setViewport ( viewport )
	-- MOAISim.pushRenderPass ( layer )
	Editor.setRenderStack( Editor.getCurrentRenderContext(), {}, { layer } )

	local gfxQuad = MOAIGfxQuad2D.new ()
	gfxQuad:setTexture ( getEditorAssetPath("moai.png") )
	gfxQuad:setRect ( -64, -64, 64, 64 )

	local prop = MOAIProp2D.new ()
	prop:setDeck ( gfxQuad )
	prop:setLoc ( 0, 80 )
	layer:insertProp ( prop )

	local font = MOAIFont.new ()
	font:loadFromTTF ( getEditorAssetPath("arialbd.ttf"), " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?!", 12, 163 )

	local textbox = MOAITextBox.new ()
	textbox:setFont ( font )
	textbox:setRect ( -160, -80, 160, 80 )
	textbox:setLoc ( 0, -100 )
	textbox:setYFlip ( true )
	textbox:setAlignment ( MOAITextBox.CENTER_JUSTIFY )
	layer:insertProp ( textbox )

	textbox:setString ( "Moai has installed correctly! <c:0F0>Check out the samples folder.<c>" )
	textbox:spool ()

	function twirlingTowardsFreedom ()
		while true do
			MOAIThread.blockOnAction ( prop:moveRot ( 360, 1.5 ))
			MOAIThread.blockOnAction ( prop:moveRot ( -360, 1.5 ))
		end
	end

	local thread = MOAIThread.new ()
	thread:run ( twirlingTowardsFreedom )

	return true
	-- return tableToDict({ status = true })
end