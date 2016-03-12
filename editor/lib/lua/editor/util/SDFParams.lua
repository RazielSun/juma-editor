--------------------------------------------------------------------------------
-- Project specific override for SDFParams
-- 
-- 
--------------------------------------------------------------------------------

local App = require("core.App")
local SDFParams = {}

local FONT_SIZE = 32


function SDFParams.padding()
    return SDFParams.threshold() * 2
end

function SDFParams.threshold()
    -- threshold is in pixels now
    return math.floor(0.25 * FONT_SIZE)
    -- return 0.45 * SDFParams.padding()
    -- return 1.1 / SDFParams.padding()
end

function SDFParams.fontSize()
    return FONT_SIZE
end

function SDFParams.outlineWidth(points, embolden)
    embolden = embolden or 0.5
    return embolden - 0.5 * points / 16
end

function SDFParams.smoothFactor()
    local scale = 0.4 / App:getContentScale()
    return scale / SDFParams.threshold()
    -- return 0.4 * SDFParams.threshold()
end

return SDFParams
