--------------------------------------------------------------------------------
-- Coroutine extensions
--------------------------------------------------------------------------------
-- skip n steps
-- step duration is defined by MOAISim settings (simulation step)
function coroutine.skip(steps)
    for i = 1, steps do
        coroutine.yield()
    end
end

-- wait given number of seconds
function coroutine.wait(time)
    while time > 0 do
        time = time - coroutine.yield()
    end
end