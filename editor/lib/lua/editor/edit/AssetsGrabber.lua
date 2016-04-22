
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
	AssetsGrabber.grabUI()
	AssetsGrabber.grabWindows()
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
	            	if string.find(file, "%.lua") then
						AssetsGrabber.setupAtlas( string.pathJoin(pathInfo.path, file), atlasses )
					elseif string.find(file, "%.png") then
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
	local cache = {}

    AssetsGrabber.findInPath( '', folders, cache, "%.ttf" )

    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
    	AssetsGrabber.findInPath( pathInfo.path, folders, cache, "%.ttf" )
    end

    for _, item in ipairs(cache) do
    	registerAssetNodeInLibrary( item, "font" )
    end
end

function AssetsGrabber.grabLayout()
	local folders = { '', 'scenes/' }
	local cache = {}

	AssetsGrabber.findInPath( '', folders, cache, "%.scene" )

    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
    	AssetsGrabber.findInPath( pathInfo.path, folders, cache, "%.scene" )
    end

    for _, item in ipairs(cache) do
    	registerAssetNodeInLibrary( item, "scene" )
    end
end

function AssetsGrabber.grabUI()
	local folders = { '', 'ui/' }
	local cache = {}

	AssetsGrabber.findInPath( '', folders, cache, "%.ui" )

    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
    	AssetsGrabber.findInPath( pathInfo.path, folders, cache, "%.ui" )
    end

    for _, item in ipairs(cache) do
    	registerAssetNodeInLibrary( item, "ui" )
    end
end

function AssetsGrabber.grabWindows()
	registerAssetNodeInLibrary( "scene", "create_scene" )
	registerAssetNodeInLibrary( "ui", "create_scene" )
	if AssetsGrabber.extension then
		AssetsGrabber.extension()
	end
end

---------------------------------------------------------------------------------
function AssetsGrabber.findInPath( path, folders, cache, match )
	for _, folder in ipairs(folders) do
		local filePath = string.pathJoin(path, folder)
		local files = MOAIFileSystem.listFiles( filePath )

		if files then
            for i, file in ipairs(files) do
            	if string.find(file, match) then
            		table.insert( cache, string.pathJoin(filePath, file) )
				end
			end
		end
	end
end

---------------------------------------------------------------------------------

return AssetsGrabber
