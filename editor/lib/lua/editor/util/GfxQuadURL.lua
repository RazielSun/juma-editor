--------------------------------------------------------------------------------
-- GfxQuadURL.lua
-- 
-- 
-- 
--------------------------------------------------------------------------------

local ResourceMgr = require("core.ResourceMgr")
local ImageDownloader = require("util.ImageDownloader")

local GfxQuadURL = class()
GfxQuadURL.__index = MOAIGfxQuad2D.getInterfaceTable()
GfxQuadURL.__moai_class = MOAIGfxQuad2D

local CACHE = MOAIEnvironment.cacheDirectory or "cache"
local CACHE_DIR = CACHE:pathJoin("gfxQuads")
local keys = {}

-- can be reused nicely
local hashWriter = MOAIHashWriterCrypto.new()

local function getKey(url)
    if url == nil then return 'nil' end

    if not keys[url] then
        hashWriter:openMD5()
        hashWriter:write(url)
        hashWriter:close()
        keys[url] = hashWriter:getHashHex()
    end
    return keys[url]
end

local function getFilename(key)
    return CACHE_DIR:pathJoin(key .. ".cache")
end

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
function GfxQuadURL:init()

end

---
-- Initializer. Can be called multiple times.
-- @param string url            url of remote image
-- @param string placeholder    (optional) local image name to use as placholder while performing http request
-- @param number width          (optional)
-- @param number height         (optional)
-- @param string key            (optional) key to use as file name in caches directory. If not set, then md5 of url is used
function GfxQuadURL:initialize(url, placeholder, width, height, key)
    if self.__url then
        ImageDownloader.cancelTask(self.__url, self:getFilename())
    end

    self.__placeholder = placeholder
    self.__key = key or getKey(url)
    self.__url = url
    self.width = width
    self.height = height

    self:affirm(url)
end


function GfxQuadURL:affirm(url)
    local path = self:getFilename()
    if MOAIFileSystem.checkFileExists(path) then
        log.info("GfxQuadURL: already cached", path)
        self:showImage(path)
        return
    end

    self:showImage(self.__placeholder)
    self:load(url)
end


function GfxQuadURL:showImage(path)
    if not path then return end

    local texture = ResourceMgr:getTexture(path)
    if not texture then return end

    local tw, th = texture:getSize()
    local scale = texture.scale or 1
    local width = self.width or (tw / scale)
    local height = self.height or (th / scale)

    self:setUVRect(0, 1, 1, 0)
    self:setRect(-0.5 * width, -0.5 * height, 0.5 * width, 0.5 * height)
    self:setTexture(texture)
    self.texture = texture
end

function GfxQuadURL:load(url)
    ImageDownloader.pushHttpTask(url, self:getFilename(), self.onFinish, self)
end

function GfxQuadURL:onFinish(image, cancelled)    
    if not cancelled then
        local texture = MOAITexture.new()
        local path = self:getFilename()
        texture:load(image)
        ResourceMgr:setTexture(texture, path)
        
        self:showImage(path)
    end
end

function GfxQuadURL:getFilename()
    return getFilename(self.__key)
end

function GfxQuadURL.getPathForUrl(url)
    return getFilename(getKey(url))
end


return GfxQuadURL
