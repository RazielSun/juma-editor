scene = nil

function onLoad()
	scene = EditorLayoutMgr:setupScene()
end

function onResize( width, height )
	if scene then
		scene:resize( width, height )
	end
end