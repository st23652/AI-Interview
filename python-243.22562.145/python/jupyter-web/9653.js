"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[9653],{69653:(T,f,p)=>{function a(n,t,i){return t(i),i(n,t)}p.r(f),p.d(f,{elm:()=>W});var u=/[a-z]/,v=/[A-Z]/,h=/[a-zA-Z0-9_]/,l=/[0-9]/,k=/[0-9A-Fa-f]/,m=/[-&*+.\\/<>=?^|:]/,g=/[(),[\]{}]/,d=/[ \v\f]/;function e(){return function(n,t){if(n.eatWhile(d))return null;var i=n.next();if(g.test(i))return"{"===i&&n.eat("-")?a(n,t,w(1)):"["===i&&n.match("glsl|")?a(n,t,y):"builtin";if("'"===i)return a(n,t,E);if('"'===i)return n.eat('"')?n.eat('"')?a(n,t,o):"string":a(n,t,x);if(v.test(i))return n.eatWhile(h),"type";if(u.test(i)){var r=1===n.pos;return n.eatWhile(h),r?"def":"variable"}if(l.test(i)){if("0"===i){if(n.eat(/[xX]/))return n.eatWhile(k),"number"}else n.eatWhile(l);return n.eat(".")&&n.eatWhile(l),n.eat(/[eE]/)&&(n.eat(/[-+]/),n.eatWhile(l)),"number"}return m.test(i)?"-"===i&&n.eat("-")?(n.skipToEnd(),"comment"):(n.eatWhile(m),"keyword"):"_"===i?"keyword":"error"}}function w(n){return 0==n?e():function(t,i){for(;!t.eol();){var r=t.next();if("{"==r&&t.eat("-"))++n;else if("-"==r&&t.eat("}")&&0===--n)return i(e()),"comment"}return i(w(n)),"comment"}}function o(n,t){for(;!n.eol();){if('"'===n.next()&&n.eat('"')&&n.eat('"'))return t(e()),"string"}return"string"}function x(n,t){for(;n.skipTo('\\"');)n.next(),n.next();return n.skipTo('"')?(n.next(),t(e()),"string"):(n.skipToEnd(),t(e()),"error")}function E(n,t){for(;n.skipTo("\\'");)n.next(),n.next();return n.skipTo("'")?(n.next(),t(e()),"string"):(n.skipToEnd(),t(e()),"error")}function y(n,t){for(;!n.eol();){if("|"===n.next()&&n.eat("]"))return t(e()),"string"}return"string"}var b={case:1,of:1,as:1,if:1,then:1,else:1,let:1,in:1,type:1,alias:1,module:1,where:1,import:1,exposing:1,port:1};const W={name:"elm",startState:function(){return{f:e()}},copyState:function(n){return{f:n.f}},token:function(n,t){var i=t.f(n,function(R){t.f=R}),r=n.current();return b.hasOwnProperty(r)?"keyword":i},languageData:{commentTokens:{line:"--"}}}}}]);