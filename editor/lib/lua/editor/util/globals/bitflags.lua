--------------------------------------------------------------------------------
-- Bit flags helpers
--------------------------------------------------------------------------------
bitflags = {}
function bitflags.test(set, flag)
    return set % (2 * flag) >= flag
end

function bitflags.set(set, flag)
    if set % (2 * flag) >= flag then
        return set
    end
    return set + flag
end

function bitflags.clear(set, flag)
    if set % (2 * flag) >= flag then
        return set - flag
    end
    return set
end
