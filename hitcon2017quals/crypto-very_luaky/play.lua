function play(prev)
    if rn == nil then
        rn = 0
        start = 1
        tab = {}
        mode = 0
    else
        rn = rn + 1
    end

    if prev == -1 then
        alp_low = 0
        alp_high = 0xffffffff
        alp_myprev = 0
        alp_myguess = 0
        alp_prev2 = 0
        ns = ""
        noz_rnd = nil
        sm = {}
        
        if rn < 1100000 then
            for i = 1, 25000, 1 do
                t = start
                local x = {}
                for j = 1, 50, 1 do
                    t = (t * 48271) % 0x7fffffff
                    x[#x+1] = tostring(t % 3)
                end
                tab[table.concat(x, "")] = t
                start = (start * 1467418072) % 0x7fffffff
            end
        end
        
        if rn == 0 then
            mode = 1
        elseif rn == 100000 then
            mode = 2
        elseif rn == 1100000 then
            mode = 3
        elseif rn >= 2100000 then
            mode = 4
        end
    end
    
    if mode == 1 then
        if prev == -1 then
            return 1
        end
        
        return prev
    elseif mode == 2 then
        if alp_prev2 == (prev - alp_myprev + 3) % 3 then
            if alp_high > 0x61C88647 then
                alp_high = 0x61C88647
            end
        else
            if alp_low < 0x61C88647 then
                alp_low = 0x61C88647
            end
        end
        
        alp_low = alp_low + alp_myguess + 0x9e3779b9
        if alp_low >= 0x100000000 then
            alp_low = alp_low - 0x100000000
        end
        
        alp_high = alp_high + alp_myguess + 0x9e3779b9
        if alp_high >= 0x100000000 then
            alp_high = alp_high - 0x100000000
        end
        
        alp_prev2 = prev
        alp_myprev = alp_myguess
        
        if alp_low < 0x61C88647 then
            alp_myguess = (alp_prev2 + alp_myprev + 2) % 3
        else
            alp_myguess = (alp_prev2 + alp_myprev + 1) % 3
        end
        
        return alp_myguess
    elseif mode == 3 then
        if noz_rnd == nil then
            if string.len(ns) < 50 then
                ns = ns .. tostring(prev)
            else
                ns = string.sub(ns, 2) .. tostring(prev)
            end
            
            if tab[ns] ~= nil then
                noz_rnd = tab[ns]
                noz_rnd = (noz_rnd * 48271) % 0x7fffffff
            end
        else
            noz_rnd = (noz_rnd * 48271) % 0x7fffffff
            res = (noz_rnd + 2) % 3
            return res
        end
    elseif mode == 4 then
        if #sm < 50 then
            sm[#sm+1] = prev
        else
            goodslime = 0
            goodalpaca = 0
            for i = 2, 50, 1 do
                if (sm[i] + 1) % 3 == sm[i+1] then
                    goodslime = goodslime + 1
                end
                if sm[i] == sm[i+1] or (sm[i] + 2) % 3 == sm[i+1] then
                    goodalpaca = goodalpaca + 1
                end
            end
            if goodslime == 48 then
                mode = 1
            elseif goodalpaca == 48 then
                mode = 2
            else
                mode = 3
            end
        end
        return 0
    end
end
