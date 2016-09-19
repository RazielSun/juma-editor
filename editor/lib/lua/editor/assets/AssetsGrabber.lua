
---------------------------------------------------------------------------------
--
-- @type AssetsGrabber
--
---------------------------------------------------------------------------------

local AssetsGrabber = {}

function AssetsGrabber.grabFromResourceMgr()
	AssetsGrabber.grabSprites()
	AssetsGrabber.grabResource( "font", "%.ttf", "fonts/" )
	AssetsGrabber.grabResource( "scene", "%.scene", "scenes/" )
	AssetsGrabber.grabResource( "ui", "%.ui", "ui/" )
	AssetsGrabber.grabResource( "prefabUI", "%.prefabUI", "ui/" )
	AssetsGrabber.grabWindows()
	if AssetsGrabber.grabProjectFiles then
		AssetsGrabber.grabProjectFiles()
	end
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

function AssetsGrabber.grabResource( name, format, path )
	local folders = { '', path }
	local cache = {}

	AssetsGrabber.findInPath( '', folders, cache, format )

    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
    	AssetsGrabber.findInPath( pathInfo.path, folders, cache, format )
    end

    for _, item in ipairs(cache) do
    	registerAssetNodeInLibrary( item, name )
    end
end

function AssetsGrabber.grabWindows()
	registerAssetNodeInLibrary( "scene", "create_scene" )
	registerAssetNodeInLibrary( "scene3d", "create_scene" )
	registerAssetNodeInLibrary( "ui", "create_scene" )
	registerAssetNodeInLibrary( "prefabUI", "create_scene" )
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
