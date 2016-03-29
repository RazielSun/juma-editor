
---------------------------------------------------------------------------------
--
-- @type AssetsGrabber
--
---------------------------------------------------------------------------------

local AssetsGrabber = {}

function AssetsGrabber.grabFromResourceMgr()
	AssetsGrabber.grabSprites()
	AssetsGrabber.grabFonts()
	AssetsGrabber.grabLayout()
end

function AssetsGrabber.grabSprites()
	local sprites = {}
	local atlasses = {}
	AssetsGrabber.findAtlases( sprites, atlasses )

	for _, atlas in ipairs(atlasses) do
		sprites[atlas.texture] = false
		for _, sprite in ipairs(atlas.frames) do
			sprites[sprite.name] = true
		end
	end

	for name, valid in pairs(sprites) do
		if valid then
			-- print("register: sprite: ", name)
			registerAssetNodeInLibrary( name, "sprite" )
		end
	end
end

function AssetsGrabber.findAtlases( sprites, atlasses )
	local scaleFactor = App:getContentScale() or 1
    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
        if pathInfo.threshold <= scaleFactor then
        	local files = MOAIFileSystem.listFiles( pathInfo.path )
        	
        	if files then
	            for i, file in ipairs(files) do
	            	if string.find(file, ".lua") then
						AssetsGrabber.setupAtlas( string.pathJoin(pathInfo.path, file), atlasses )
					elseif string.find(file, ".png") then
						sprites[file] = true
					end
				end
			end
        end
    end
end

function AssetsGrabber.setupAtlas( path, atlasses )
	local tbl = assert(loadfile(path))
    setfenv(tbl, {})
    local atlas = tbl()
    table.insert( atlasses, atlas )
end

function AssetsGrabber.grabFonts()
	local folders = { '', 'fonts/' }
	local fonts = {}

	local scaleFactor = App:getContentScale() or 1
    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
        if pathInfo.threshold <= scaleFactor then
        	for _, folder in ipairs(folders) do
        		local filePath = string.pathJoin(pathInfo.path, folder)
        		local files = MOAIFileSystem.listFiles( filePath )

        		if files then
		            for i, file in ipairs(files) do
		            	if string.find(file, ".ttf") then
		            		table.insert( fonts, string.pathJoin(folder, file) )
						end
					end
				end
        	end
        end
    end

    for _, font in ipairs(fonts) do
    	-- print("register: font: ", font)
    	registerAssetNodeInLibrary( font, "font" )
    end
end

function AssetsGrabber.grabLayout()
	local folders = { '', 'layouts/' }
	local layouts = {}

    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
    	for _, folder in ipairs(folders) do
    		local filePath = string.pathJoin(pathInfo.path, folder)
    		local files = MOAIFileSystem.listFiles( filePath )

    		if files then
	            for i, file in ipairs(files) do
	            	if string.find(file, ".layout") then
	            		table.insert( layouts, string.pathJoin(filePath, file) )
					end
				end
			end
    	end
    end

    for _, layout in ipairs(layouts) do
    	registerAssetNodeInLibrary( layout, "layout" )
    end
end

---------------------------------------------------------------------------------

return AssetsGrabber
