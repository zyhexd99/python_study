const CryptoJS = require('crypto-js');

function decrypt(t) {
    var r = {
        e:process.env.e,
        i:process.env.i
    }
var e = CryptoJS.enc.Utf8.parse(r["e"])
              , n = CryptoJS.enc.Utf8.parse(r["i"])
              , a = CryptoJS.AES.decrypt(t, e, {
iv: n,
mode: CryptoJS.mode.CBC,
padding: CryptoJS.pad.Pkcs7
            });
return a.toString(CryptoJS.enc.Utf8)
}

//请求加密
function l(t, e) {
            return t.toString().toUpperCase() > e.toString().toUpperCase() ? 1 : t.toString().toUpperCase() == e.toString().toUpperCase() ? 0 : -1
        }
function u(t) {
            for (var e = Object.keys(t).sort(l), n = "", a = 0; a < e.length; a++)
                if (void 0 !== t[e[a]])
                    if (t[e[a]] && t[e[a]]instanceof Object || t[e[a]]instanceof Array) {
                        var i = JSON.stringify(t[e[a]]);
                        n += e[a] + i
                    } else
                        n += e[a] + t[e[a]];
            return n
}
function encrypt(t) {
for (var e in t)
"" !== t[e] && void 0 !== t[e] || delete t[e];
s = process.env.s
var n = s+ u(t);
return CryptoJS.MD5(n).toString().toLocaleLowerCase()
}


