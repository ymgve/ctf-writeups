var flag = "SECT{1ts_1n_th4T_pl4Ce_Wh3re_1_Pu7_tH4t_Th1ng_th4T_t1m3,}"
var readline = require('readline');
var rl = readline.createInterface(process.stdin, process.stdout);

var Jail = (function() {
    var rv = {};

    function call(number) {
        var hangup = process.exit;
        var line = "";

        if(number == 911){
            console.log("Invalid number");
            ask();
            return;
        }

        var flag,Array,Boolean,Date,global,Error,EvalError,Function,Number,Object,RangeError,ReferenceError,String,SyntaxError,TypeError,URIError,decodeURI,decodeURIComponent,encodeURI,encodeURIComponent,isFinite,isNaN,parseFloat,parseInt,ArrayBuffer,Buffer,DTRACE_HTTP_CLIENT_REQUEST,DTRACE_HTTP_CLIENT_RESPONSE,DTRACE_HTTP_SERVER_REQUEST,DTRACE_HTTP_SERVER_RESPONSE,DTRACE_NET_SERVER_CONNECTION,DTRACE_NET_STREAM_END,DataView,Float32Array,Float64Array,Int16Array,Int32Array,Int8Array,Map,Promise,Proxy,Set,Symbol,Uint16Array,Uint32Array,Uint8Array,Uint8ClampedArray,WeakMap,WeakSet,assert,clearImmediate,clearInterval,clearTimeout,escape,events,require,setImmediate,setInterval,setTimeout,stream,unescape,__defineGetter__,__defineSetter__,__lookupGetter__,__lookupSetter__,constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf;

        if(new RegExp(/[\[\]\.\\]/).test(number)){
            console.log("Dangerous characters detected");
            hangup();
            return;
        }

        arguments = undefined;

        console.log("Calling "+eval(number)+"... Nobody picks up!");
        hangup();
    };
    rv.call = call;
    rv.toString = function(){return rv.call.toString()};

    return rv;
})();

template = `_____________________________
     ||   ||     ||   ||
     ||   ||, , ,||   ||
     ||  (||/|/(\/||/  ||
     ||  ||| _'_-¦|||  ||
     ||   || o o ||   ||
     ||  (||  - -¦||)  ||
     ||   ||  =  ||   ||
     ||   ||\\___/||   ||
     ||___||) , (||___||
    /||---||-\\_/-||---||\\
   / ||--_||_____||_--|| \\
  (_(||)-|S555-4202|-(||)_)
|"""""""""""""""""""""""""""|
| "You get one call, UNO."  |
 """""""""""""""""""""""""""
 Phone #> `;

function ask(){
    rl.question(template,function(answer){
        Jail.call(answer);
    });
}

ask();

