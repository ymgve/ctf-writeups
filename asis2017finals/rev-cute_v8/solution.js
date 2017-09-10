function get_flag() {
    s = "ASIS{";
    var r0 = 65;
    var r7 = 0;
    for (var r8 = 0; r8 <= 20; r8++) {
        var r9 = 47;
        r9 = r9 < r0;
        if (!(r9 < 58)) {
            r9 = 64;
            r9 = r9 < r0;
            if (!(r9 < 90)) {
                r9 = 96;
                r9 = r9 < r0;
                if (r9 < 123) {
                    s += String.fromCharCode(r0);
                }
            } else {
                s += String.fromCharCode(r0);
            }
        } else {
            s += String.fromCharCode(r0);
        }
        
        if (r7 == 2) {
            r0 ^= 4;
        }
        
        if (r7 >= 1) {
            r0 ^= 3;
        }
        
        r0 += 5;
        
        r9 = 122;
        if (r9 < r0) {
            r7 += 1;
            s += "_";
            r0 = 66;
        }
        
        if (r0 < 48) {
            r0 += 30;
        }
    }
    
    s += "}";
    
    return s;
}

console.log(get_flag());