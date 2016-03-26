
---------------------------------------------------------------------------------
--
-- @type AssetsGrabber
--
---------------------------------------------------------------------------------

local AssetsGrabber = {}

-- # HARDCODE

function AssetsGrabber.grabFromResourceMgr()
	local workDir = PROJECT_GAME_PATH
	if not workDir then return end
	print()
	print()
	workDir = workDir .. "/assets"
	print('WORKING DIR:', workDir, MOAIFileSystem.getWorkingDirectory() )
	local dirs = MOAIFileSystem.listDirectories( workDir )
	local files = MOAIFileSystem.listFiles( workDir )

	for i, v in ipairs(dirs) do
		print("DIRS:",i,v)
	end
	print()
	for i, v in ipairs(files) do
		print("FILES:",i,v)
	end
	print()

	local fileName = ''

    local scaleFactor = App:getContentScale() or 1
    for i, pathInfo in ipairs(ResourceMgr.resourceDirectories) do
        if pathInfo.threshold <= scaleFactor then
            local filePath = string.pathJoin(pathInfo.path, fileName)
            print("filePath:", scaleFactor, filePath)
        end
    end

	registerAssetNodeInLibrary( "moai.png", "sprite" )
	registerAssetNodeInLibrary( "arialbd.ttf", "font" )
end

---------------------------------------------------------------------------------

return AssetsGrabber


-- function ResourceMgr:getResourceFilePath(fileName)
--     local cache = self.filepathCache
--     if cache[fileName] then
--         if cache[fileName] == NOT_FOUND then
--             return nil
--         else
--             return unpack(cache[fileName])
--         end
--     end

--     if MOAIFileSystem.checkFileExists(fileName) then
--         cache[fileName] = {fileName, 1} 
--         return fileName, 1
--     end


--     cache[fileName] = NOT_FOUND
--     return nil
-- end