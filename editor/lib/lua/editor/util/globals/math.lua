---------------------------------------------------------------------------------
-- Math module extensions
---------------------------------------------------------------------------------

---
-- Calculate the distance.
-- @param x0 Start position.
-- @param y0 Start position.
-- @param x1 (option)End position (note: default value is 0)
-- @param y1 (option)End position (note: default value is 0)
-- @return distance
function math.distance( x0, y0, x1, y1 )
    if not x1 then x1 = 0 end
    if not y1 then y1 = 0 end

    local dX = x1 - x0
    local dY = y1 - y0
    local dist = math.sqrt((dX * dX) + (dY * dY))
    return dist
end

function math.distanceSQ( x0, y0, x1, y1 )
    if not x1 then x1 = 0 end
    if not y1 then y1 = 0 end

    local dX = x1 - x0
    local dY = y1 - y0
    return ((dX * dX) + (dY * dY))
end

function math.mapLinear(value, ax, bx, ay, by)
    assert(ax ~= bx, "ax and bx should be different")
    return ay + ((value - ax) / (bx - ax)) * (by - ay)
end


---
-- Get the normal vector
-- @param x
-- @param y
-- @return x/d, y/d
function math.normalize( x, y )
    local d = math.distance( x, y )
    return x/d, y/d
end

function math.clamp(x, min, max)
    return math.max(min, math.min(x, max))
end

function math.sign(x)
    return x < 0 and -1 or 1
end

---
-- Round a number to a full number of snaps
-- @param number x
-- @param number (optional) snap, default is 1
function math.round(x, snap)
    snap = snap or 1
    return snap * math.floor(x / snap + 0.5)
end

---
-- Floor a number to a full number of snaps
-- @param number x
-- @param number (optional) snap, default is 1
function math.floorTo(x, snap)
    snap = snap or 1
    return snap * math.floor(x / snap)
end

function math.nextPot(x)
    local n = math.ceil(math.log(x)/math.log(2))
    return math.pow(2, n)
end


---
-- Returns random integer in [lower, upper] bounds
-- @param lower
-- @param upper
local rand = MOAIMath and MOAIMath.randSFMT
function math.randomInt(lower, upper)
    if rand then
        return math.round( rand(lower - 0.5, upper + 0.5), 1 )
    end
    return math.random(lower, upper)
end

---
-- vec with random length and direction
-- @param minLength     min length
-- @param maxLength     max lenght
-- @param minAngle      min angle in radians. min < max
-- @param maxAngle      max angle in radians. min < max
-- @return x, y
function math.randomVec(minLength, maxLength, minAngle, maxAngle)
    local a = minAngle + math.random() * (maxAngle - minAngle)
    local l = minLength + math.random() * (maxLength - minLength)
    return l * math.cos(a), l * math.sin(a)
end

---
-- Returns whether a point inside given rect
function math.inside(x, y, xMin, yMin, xMax, yMax)
    return x > xMin and x < xMax and y > yMin and y < yMax
end


---
-- Linear interpolation
function math.lerp(a, b, t)
    return a + (b - a) * t
end

---
-- Calculate shortest delta between two angles in degrees: angle2 - angle1
-- @param angle1
-- @param angle2
-- @return delta [-180, 180]
function math.angleDiff(a1, a2)
    local diff = a2 - a1
    return (diff + 180) % 360 - 180
end
