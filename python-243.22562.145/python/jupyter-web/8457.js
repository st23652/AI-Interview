"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[8457],{48457:(y,t,a)=>{function r(n){for(var e={},i=n.split(" "),l=0;l<i.length;++l)e[i[l]]=!0;return e}a.r(t),a.d(t,{modelica:()=>w});var u=r("algorithm and annotation assert block break class connect connector constant constrainedby der discrete each else elseif elsewhen encapsulated end enumeration equation expandable extends external false final flow for function if import impure in initial inner input loop model not operator or outer output package parameter partial protected public pure record redeclare replaceable return stream then true type when while within"),c=r("abs acos actualStream asin atan atan2 cardinality ceil cos cosh delay div edge exp floor getInstanceName homotopy inStream integer log log10 mod pre reinit rem semiLinear sign sin sinh spatialDistribution sqrt tan tanh"),f=r("Real Boolean Integer String"),s=[].concat(Object.keys(u),Object.keys(c),Object.keys(f)),p=/[;=\(:\),{}.*<>+\-\/^\[\]]/,d=/(:=|<=|>=|==|<>|\.\+|\.\-|\.\*|\.\/|\.\^)/,o=/[0-9]/,k=/[_a-zA-Z]/;function h(n,e){return n.skipToEnd(),e.tokenize=null,"comment"}function b(n,e){for(var l,i=!1;l=n.next();){if(i&&"/"==l){e.tokenize=null;break}i="*"==l}return"comment"}function v(n,e){for(var l,i=!1;null!=(l=n.next());){if('"'==l&&!i){e.tokenize=null,e.sol=!1;break}i=!i&&"\\"==l}return"string"}function g(n,e){for(n.eatWhile(o);n.eat(o)||n.eat(k););var i=n.current();return!e.sol||"package"!=i&&"model"!=i&&"when"!=i&&"connector"!=i?e.sol&&"end"==i&&e.level>0&&e.level--:e.level++,e.tokenize=null,e.sol=!1,u.propertyIsEnumerable(i)?"keyword":c.propertyIsEnumerable(i)?"builtin":f.propertyIsEnumerable(i)?"atom":"variable"}function z(n,e){for(;n.eat(/[^']/););return e.tokenize=null,e.sol=!1,n.eat("'")?"variable":"error"}function m(n,e){return n.eatWhile(o),n.eat(".")&&n.eatWhile(o),(n.eat("e")||n.eat("E"))&&(n.eat("-")||n.eat("+"),n.eatWhile(o)),e.tokenize=null,e.sol=!1,"number"}const w={name:"modelica",startState:function(){return{tokenize:null,level:0,sol:!0}},token:function(n,e){if(null!=e.tokenize)return e.tokenize(n,e);if(n.sol()&&(e.sol=!0),n.eatSpace())return e.tokenize=null,null;var i=n.next();if("/"==i&&n.eat("/"))e.tokenize=h;else if("/"==i&&n.eat("*"))e.tokenize=b;else{if(d.test(i+n.peek()))return n.next(),e.tokenize=null,"operator";if(p.test(i))return e.tokenize=null,"operator";if(k.test(i))e.tokenize=g;else if("'"==i&&n.peek()&&"'"!=n.peek())e.tokenize=z;else if('"'==i)e.tokenize=v;else{if(!o.test(i))return e.tokenize=null,"error";e.tokenize=m}}return e.tokenize(n,e)},indent:function(n,e,i){if(null!=n.tokenize)return null;var l=n.level;return/(algorithm)/.test(e)&&l--,/(equation)/.test(e)&&l--,/(initial algorithm)/.test(e)&&l--,/(initial equation)/.test(e)&&l--,/(end)/.test(e)&&l--,l>0?i.unit*l:0},languageData:{commentTokens:{line:"//",block:{open:"/*",close:"*/"}},autocomplete:s}}}}]);