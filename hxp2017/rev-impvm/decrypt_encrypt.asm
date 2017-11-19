function 0
        call 252
        loadi 0
        call 8
        loadi 1
        call 8
        loadi 2
        call 8
        loadi 3
        call 8
        call 253
end

function 1                      ; xor(a, b)
        loadi 0
        dup 1
        loadi 0
        dup 1
        or
        loadi 0
        dup 2
        loadi 0
        dup 2
        and
        not
        and
end

function 2                      ; add(a, b)
        loadi 0
        dup 1
        loadi 0
        dup 1
label1
        call 1
        loadi 0
        dup 2
        loadi 0
        dup 2
        and
        shl 1
        loadi 0
        dup 0
        jmpz label2
        loadi 0
        place 2
        loadi 0
        place 0
        jmp label1
label2
        pop
end

function 3                      ; get key via index
        loadi 0
        dup 0
        loadi 3
        and
        loadi 0
        dup 0
        shr 1
        loadram 4
        loadi 0
        dup 1
        loadi 1
        and
        jmpz label1
        shl 32
label1
        shr 32
end

function 4                      ; do encrypt round
        loadi 0
        dup 0
        shr 32
        loadi 0
        dup 1
        shl 32
        shr 32
        
        loadi 0
        dup 0
        shl 4
        loadi 0
        dup 1
        shr 5
        call 1
        loadi 0
        place 1
        pop
        
        call 2
        loadi 0
        place 0
        loadi 0
        loadram 8
        call 3
        call 2
        loadi 0
        place 1
        pop
        call 1
        loadi 0
        place 1
        pop
        loadi 0
        dup 2
        call 2
        shl 32
        shr 32
        loadi 0
        place 3
        pop
        pop
        
        loadi 0
        loadram 8
        loadi 0
        loadram 9
        call 2
        loadi 0
        saveram 8
        pop
        pop
        
        loadi 0
        dup 1
        shl 4
        loadi 0
        dup 2
        shr 5
        call 1
        loadi 0
        place 1
        pop
        
        loadi 0
        dup 2
        call 2
        loadi 0
        place 1
        pop
        
        loadi 0
        loadram 8
        loadi 0
        dup 0
        shr 11
        call 3
        loadi 0
        place 0
        call 2
        loadi 0
        place 1
        pop
        call 1
        
        loadi 0
        place 1
        pop
        call 2
        shl 32
        shr 32
        
        loadi 0
        dup 3
        shl 32
        or
end

function 5
        loadi 0
        loadi 0
        saveram 8
        
        loadi 1
        shl 31
label1
        loadi 0
        dup 1
        loadram 0
        call 4
        loadi 0
        dup 3
        saveram 0
        pop
        shr 1
        loadi 0
        dup 0
        jmpz label2
        jmp label1
label2
end

function 6
        loadi 0
        dup 0
        not
        loadi 1
        call 2
        loadi 0
        dup 4
        call 2
end

function 7
        loadi 0
        dup 0
        shr 32
        loadi 0
        dup 1
        shl 32
        shr 32

        loadi 0
        dup 1
        shl 4
        loadi 0
        dup 2
        shr 5
        call 1
        loadi 0
        place 1
        pop
        
        loadi 0
        dup 2
        call 2
        loadi 0
        place 1
        pop
        
        loadi 0
        loadram 8
        loadi 0
        dup 0
        shr 11
        call 3
        loadi 0
        place 0
        call 2
        loadi 0
        place 1
        pop
        call 1
        
        loadi 0
        dup 3
        loadi 0
        dup 1
        call 6
        shl 32
        shr 32
        loadi 0
        place 5
        pop
        pop
        pop
        pop
        pop

        loadi 0
        loadram 8
        loadi 0
        loadram 9
        call 6
        loadi 0
        saveram 8
        pop
        pop
        
        loadi 0
        dup 0
        shl 4
        loadi 0
        dup 1
        shr 5
        call 1
        loadi 0
        place 1
        pop
        
        call 2
        loadi 0
        place 0
        
        loadi 0
        loadram 8
        call 3
        call 2
        loadi 0
        place 1
        pop
        call 1
        
        loadi 0
        dup 4
        loadi 0
        dup 1
        call 6
        shl 32
        shr 32
        
        shl 32
        loadi 0
        dup 6
        or
end

function 8
        loadi 0
        loadram 10
        loadi 0
        saveram 8
        
        loadi 1
        shl 31
label1
        loadi 0
        dup 1
        loadram 0
        call 7
        loadi 0
        dup 3
        saveram 0
        pop
        shr 1
        loadi 0
        dup 0
        jmpz label2
        jmp label1
label2
end

        qword 0x64c729478f8e9f5a
        qword 0x4444444433333333
        qword 0x1111111122222222
        qword 0x1111111122222222
        qword 0x123456789ABCDEF0
        qword 0x1F2E3D4C5B6A7988
        qword 0
        qword 0
        qword 0          ; sum
        qword 0x9e3779b9 ; delta
        qword 0x13c6ef3720 ; decryptsum
        
        blankram 16
