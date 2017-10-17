coro = {}
coro.main = function() end
coro.current = coro.main

-- function to create a new coroutine
function coro.create(f)
    local co = function(val)
        f(val)
        error("coroutine ended")
    end
    return coroutine.wrap(co)
end

-- function to transfer control to a coroutine
function coro.transfer(co, val)
    if coro.current == coro.main then
        return coroutine.yield(co, val)
    end

    -- dispatching loop
    while true do
        coro.current = co
        if co == coro.main then
            return val
        end
        co, val = co(val)
    end
end

function call1cc(f)
    -- save the continuation "creator"
    local ccoro = coro.current
    -- invoking the continuation transfers control
    -- back to its creator
    local cont = function(val)
        if ccoro == nil then
            error("one shot continuation called twice")
        end
        coro.transfer(ccoro, val)
    end
    -- when a continuation is captured,
    -- a new coroutine is created and dispatched
    local val
    val = coro.transfer(coro.create(function()
        local v = f(cont)
        cont(v)
    end))
    -- when control is transfered back, the continuation
    -- was "shot" and must be invalidated
    ccoro = nil
    -- the value passed to the continuation
    -- is the return value of call1/cc
    return val
end