--------------------------------------------------------------------------------
-- GfxQuadURLMutlitexture
-- 
-- 
--------------------------------------------------------------------------------

---
--  Used with only single texture, without atlas !!!
--

local GfxQuadURL = require("util.GfxQuadURL")

local GfxQuadURLMutlitexture = class(GfxQuadURL)

function GfxQuadURLMutlitexture:init(...)
    GfxQuadURL.init(self, ...)
end

function GfxQuadURLMutlitexture:affirmMultitexture()
    local multitexture = self.multitexture
    if not multitexture then
        multitexture = MOAIMultiTexture.new()
        multitexture:reserve(2)
        GfxQuadURL.setTexture(self, multitexture)
        self.multitexture = multitexture
    end
    return multitexture
end

function GfxQuadURLMutlitexture:setTexture(texture)
    local multi = self:affirmMultitexture()
    multi:setTexture(1, texture)
end

function GfxQuadURLMutlitexture:setMask(texture)
    local multi = self:affirmMultitexture()
    multi:setTexture(2, texture)
end

return GfxQuadURLMutlitexture