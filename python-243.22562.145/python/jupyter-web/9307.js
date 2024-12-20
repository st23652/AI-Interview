"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[9307,84],{49307:function(N,r,M){var o,E=this&&this.__extends||(o=function(l,f){return(o=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(v,y){v.__proto__=y}||function(v,y){for(var g in y)Object.prototype.hasOwnProperty.call(y,g)&&(v[g]=y[g])})(l,f)},function(l,f){if("function"!=typeof f&&null!==f)throw new TypeError("Class extends value "+String(f)+" is not a constructor or null");function v(){this.constructor=l}o(l,f),l.prototype=null===f?Object.create(f):(v.prototype=f.prototype,new v)}),w=this&&this.__assign||function(){return w=Object.assign||function(o){for(var l,f=1,v=arguments.length;f<v;f++)for(var y in l=arguments[f])Object.prototype.hasOwnProperty.call(l,y)&&(o[y]=l[y]);return o},w.apply(this,arguments)},T=this&&this.__read||function(o,l){var f="function"==typeof Symbol&&o[Symbol.iterator];if(!f)return o;var y,O,v=f.call(o),g=[];try{for(;(void 0===l||l-- >0)&&!(y=v.next()).done;)g.push(y.value)}catch(_){O={error:_}}finally{try{y&&!y.done&&(f=v.return)&&f.call(v)}finally{if(O)throw O.error}}return g},a=this&&this.__spreadArray||function(o,l,f){if(f||2===arguments.length)for(var g,v=0,y=l.length;v<y;v++)(g||!(v in l))&&(g||(g=Array.prototype.slice.call(l,0,v)),g[v]=l[v]);return o.concat(g||Array.prototype.slice.call(l))},n=this&&this.__values||function(o){var l="function"==typeof Symbol&&Symbol.iterator,f=l&&o[l],v=0;if(f)return f.call(o);if(o&&"number"==typeof o.length)return{next:function(){return o&&v>=o.length&&(o=void 0),{value:o&&o[v++],done:!o}}};throw new TypeError(l?"Object is not iterable.":"Symbol.iterator is not defined.")};Object.defineProperty(r,"__esModule",{value:!0}),r.SafeHandler=r.SafeMathDocumentMixin=void 0;var e=M(111);function i(o){var l;return l=function(f){function v(){for(var y,g,O=[],_=0;_<arguments.length;_++)O[_]=arguments[_];var t=f.apply(this,a([],T(O),!1))||this;t.safe=new t.options.SafeClass(t,t.options.safeOptions);var s=t.constructor.ProcessBits;s.has("safe")||s.allocate("safe");try{for(var c=n(t.inputJax),h=c.next();!h.done;h=c.next()){var d=h.value;d.name.match(/MathML/)?(d.mathml.filterAttribute=t.safe.mmlAttribute.bind(t.safe),d.mathml.filterClassList=t.safe.mmlClassList.bind(t.safe)):d.name.match(/TeX/)&&d.postFilters.add(t.sanitize.bind(d),-5.5)}}catch(p){y={error:p}}finally{try{h&&!h.done&&(g=c.return)&&g.call(c)}finally{if(y)throw y.error}}return t}return E(v,f),v.prototype.sanitize=function(y){y.math.root=this.parseOptions.root,y.document.safe.sanitize(y.math,y.document)},v}(o),l.OPTIONS=w(w({},o.OPTIONS),{safeOptions:w({},e.Safe.OPTIONS),SafeClass:e.Safe}),l}r.SafeMathDocumentMixin=i,r.SafeHandler=function u(o){return o.documentClass=i(o.documentClass),o}},4718:function(N,r,M){var E=this&&this.__values||function(a){var n="function"==typeof Symbol&&Symbol.iterator,e=n&&a[n],i=0;if(e)return e.call(a);if(a&&"number"==typeof a.length)return{next:function(){return a&&i>=a.length&&(a=void 0),{value:a&&a[i++],done:!a}}};throw new TypeError(n?"Object is not iterable.":"Symbol.iterator is not defined.")},w=this&&this.__read||function(a,n){var e="function"==typeof Symbol&&a[Symbol.iterator];if(!e)return a;var u,l,i=e.call(a),o=[];try{for(;(void 0===n||n-- >0)&&!(u=i.next()).done;)o.push(u.value)}catch(f){l={error:f}}finally{try{u&&!u.done&&(e=i.return)&&e.call(i)}finally{if(l)throw l.error}}return o};Object.defineProperty(r,"__esModule",{value:!0}),r.SafeMethods=void 0;var T=M(21108);r.SafeMethods={filterURL:function(a,n){var e=(n.match(/^\s*([a-z]+):/i)||[null,""])[1].toLowerCase(),i=a.allow.URLs;return"all"===i||"safe"===i&&(a.options.safeProtocols[e]||!e)?n:null},filterClassList:function(a,n){var e=this;return n.trim().replace(/\s\s+/g," ").split(/ /).map(function(u){return e.filterClass(a,u)||""}).join(" ").trim().replace(/\s\s+/g,"")},filterClass:function(a,n){var e=a.allow.classes;return"all"===e||"safe"===e&&n.match(a.options.classPattern)?n:null},filterID:function(a,n){var e=a.allow.cssIDs;return"all"===e||"safe"===e&&n.match(a.options.idPattern)?n:null},filterStyles:function(a,n){var e,i,u,o;if("all"===a.allow.styles)return n;if("safe"!==a.allow.styles)return null;var l=a.adaptor,f=a.options;try{var v=l.node("div",{style:n}),y=l.node("div");try{for(var g=E(Object.keys(f.safeStyles)),O=g.next();!O.done;O=g.next()){var _=O.value;if(f.styleParts[_])try{for(var t=(u=void 0,E(["Top","Right","Bottom","Left"])),s=t.next();!s.done;s=t.next()){var d,h=_+s.value;(d=this.filterStyle(a,h,v))&&l.setStyle(y,h,d)}}catch(p){u={error:p}}finally{try{s&&!s.done&&(o=t.return)&&o.call(t)}finally{if(u)throw u.error}}else(d=this.filterStyle(a,_,v))&&l.setStyle(y,_,d)}}catch(p){e={error:p}}finally{try{O&&!O.done&&(i=g.return)&&i.call(g)}finally{if(e)throw e.error}}n=l.allStyles(y)}catch{n=""}return n},filterStyle:function(a,n,e){var i=a.adaptor.getStyle(e,n);if("string"!=typeof i||""===i||i.match(/^\s*calc/)||i.match(/javascript:/)&&!a.options.safeProtocols.javascript||i.match(/data:/)&&!a.options.safeProtocols.data)return null;var u=n.replace(/Top|Right|Left|Bottom/,"");return a.options.safeStyles[n]||a.options.safeStyles[u]?this.filterStyleValue(a,n,i,e):null},filterStyleValue:function(a,n,e,i){var u=a.options.styleLengths[n];if(!u)return e;if("string"!=typeof u)return this.filterStyleLength(a,n,e);var o=this.filterStyleLength(a,u,a.adaptor.getStyle(i,u));return o?(a.adaptor.setStyle(i,u,o),a.adaptor.getStyle(i,n)):null},filterStyleLength:function(a,n,e){if(!e.match(/^(.+)(em|ex|ch|rem|px|mm|cm|in|pt|pc|%)$/))return null;var i=(0,T.length2em)(e,1),u=a.options.styleLengths[n],o=w(Array.isArray(u)?u:[-a.options.lengthMax,a.options.lengthMax],2),l=o[0],f=o[1];return l<=i&&i<=f?e:(i<l?l:f).toFixed(3).replace(/\.?0+$/,"")+"em"},filterFontSize:function(a,n){return this.filterStyleLength(a,"fontSize",n)},filterSizeMultiplier:function(a,n){var e=w(a.options.scriptsizemultiplierRange||[-1/0,1/0],2),i=e[0],u=e[1];return Math.min(u,Math.max(i,parseFloat(n))).toString()},filterScriptLevel:function(a,n){var e=w(a.options.scriptlevelRange||[-1/0,1/0],2),i=e[0],u=e[1];return Math.min(u,Math.max(i,parseInt(n))).toString()},filterData:function(a,n,e){return e.match(a.options.dataPattern)?n:null}}},111:function(N,r,M){var E=this&&this.__assign||function(){return E=Object.assign||function(e){for(var i,u=1,o=arguments.length;u<o;u++)for(var l in i=arguments[u])Object.prototype.hasOwnProperty.call(i,l)&&(e[l]=i[l]);return e},E.apply(this,arguments)},w=this&&this.__values||function(e){var i="function"==typeof Symbol&&Symbol.iterator,u=i&&e[i],o=0;if(u)return u.call(e);if(e&&"number"==typeof e.length)return{next:function(){return e&&o>=e.length&&(e=void 0),{value:e&&e[o++],done:!e}}};throw new TypeError(i?"Object is not iterable.":"Symbol.iterator is not defined.")};Object.defineProperty(r,"__esModule",{value:!0}),r.Safe=void 0;var T=M(80084),a=M(4718),n=function(){function e(i,u){this.filterAttributes=new Map([["href","filterURL"],["src","filterURL"],["altimg","filterURL"],["class","filterClassList"],["style","filterStyles"],["id","filterID"],["fontsize","filterFontSize"],["mathsize","filterFontSize"],["scriptminsize","filterFontSize"],["scriptsizemultiplier","filterSizeMultiplier"],["scriptlevel","filterScriptLevel"],["data-","filterData"]]),this.filterMethods=E({},a.SafeMethods),this.adaptor=i.adaptor,this.options=u,this.allow=this.options.allow}return e.prototype.sanitize=function(i,u){try{i.root.walkTree(this.sanitizeNode.bind(this))}catch(o){u.options.compileError(u,i,o)}},e.prototype.sanitizeNode=function(i){var u,o,l=i.attributes.getAllAttributes();try{for(var f=w(Object.keys(l)),v=f.next();!v.done;v=f.next()){var y=v.value,g=this.filterAttributes.get(y);if(g){var O=this.filterMethods[g](this,l[y]);O?O!==("number"==typeof O?parseFloat(l[y]):l[y])&&(l[y]=O):delete l[y]}}}catch(_){u={error:_}}finally{try{v&&!v.done&&(o=f.return)&&o.call(f)}finally{if(u)throw u.error}}},e.prototype.mmlAttribute=function(i,u){if("class"===i)return null;var l=this.filterAttributes.get(i)||("data-"===i.substr(0,5)?this.filterAttributes.get("data-"):null);if(!l)return u;var f=this.filterMethods[l](this,u,i);return"number"==typeof f||"boolean"==typeof f?String(f):f},e.prototype.mmlClassList=function(i){var u=this;return i.map(function(o){return u.filterMethods.filterClass(u,o)}).filter(function(o){return null!==o})},e.OPTIONS={allow:{URLs:"safe",classes:"safe",cssIDs:"safe",styles:"safe"},lengthMax:3,scriptsizemultiplierRange:[.6,1],scriptlevelRange:[-2,2],classPattern:/^mjx-[-a-zA-Z0-9_.]+$/,idPattern:/^mjx-[-a-zA-Z0-9_.]+$/,dataPattern:/^data-mjx-/,safeProtocols:(0,T.expandable)({http:!0,https:!0,file:!0,javascript:!1,data:!1}),safeStyles:(0,T.expandable)({color:!0,backgroundColor:!0,border:!0,cursor:!0,margin:!0,padding:!0,textShadow:!0,fontFamily:!0,fontSize:!0,fontStyle:!0,fontWeight:!0,opacity:!0,outline:!0}),styleParts:(0,T.expandable)({border:!0,padding:!0,margin:!0,outline:!0}),styleLengths:(0,T.expandable)({borderTop:"borderTopWidth",borderRight:"borderRightWidth",borderBottom:"borderBottomWidth",borderLeft:"borderLeftWidth",paddingTop:!0,paddingRight:!0,paddingBottom:!0,paddingLeft:!0,marginTop:!0,marginRight:!0,marginBottom:!0,marginLeft:!0,outlineTop:!0,outlineRight:!0,outlineBottom:!0,outlineLeft:!0,fontSize:[.707,1.44]})},e}();r.Safe=n},80084:function(N,r){var M=this&&this.__values||function(t){var s="function"==typeof Symbol&&Symbol.iterator,c=s&&t[s],h=0;if(c)return c.call(t);if(t&&"number"==typeof t.length)return{next:function(){return t&&h>=t.length&&(t=void 0),{value:t&&t[h++],done:!t}}};throw new TypeError(s?"Object is not iterable.":"Symbol.iterator is not defined.")},E=this&&this.__read||function(t,s){var c="function"==typeof Symbol&&t[Symbol.iterator];if(!c)return t;var d,b,h=c.call(t),p=[];try{for(;(void 0===s||s-- >0)&&!(d=h.next()).done;)p.push(d.value)}catch(S){b={error:S}}finally{try{d&&!d.done&&(c=h.return)&&c.call(h)}finally{if(b)throw b.error}}return p},w=this&&this.__spreadArray||function(t,s,c){if(c||2===arguments.length)for(var p,h=0,d=s.length;h<d;h++)(p||!(h in s))&&(p||(p=Array.prototype.slice.call(s,0,h)),p[h]=s[h]);return t.concat(p||Array.prototype.slice.call(s))};Object.defineProperty(r,"__esModule",{value:!0}),r.lookup=r.separateOptions=r.selectOptionsFromKeys=r.selectOptions=r.userOptions=r.defaultOptions=r.insert=r.copy=r.keys=r.makeArray=r.expandable=r.Expandable=r.OPTIONS=r.REMOVE=r.APPEND=r.isObject=void 0;var T={}.constructor;function a(t){return"object"==typeof t&&null!==t&&(t.constructor===T||t.constructor===n)}r.isObject=a,r.APPEND="[+]",r.REMOVE="[-]",r.OPTIONS={invalidOption:"warn",optionError:function(t,s){if("fatal"===r.OPTIONS.invalidOption)throw new Error(t);console.warn("MathJax: "+t)}};var n=function t(){};function e(t){return Object.assign(Object.create(n.prototype),t)}function u(t){return t?Object.keys(t).concat(Object.getOwnPropertySymbols(t)):[]}function o(t){var s,c,h={};try{for(var d=M(u(t)),p=d.next();!p.done;p=d.next()){var b=p.value,S=Object.getOwnPropertyDescriptor(t,b),A=S.value;Array.isArray(A)?S.value=l([],A,!1):a(A)&&(S.value=o(A)),S.enumerable&&(h[b]=S)}}catch(m){s={error:m}}finally{try{p&&!p.done&&(c=d.return)&&c.call(d)}finally{if(s)throw s.error}}return Object.defineProperties(t.constructor===n?e({}):{},h)}function l(t,s,c){var h,d;void 0===c&&(c=!0);var p=function(m){if(c&&void 0===t[m]&&t.constructor!==n)return"symbol"==typeof m&&(m=m.toString()),r.OPTIONS.optionError('Invalid option "'.concat(m,'" (no default value).'),m),"continue";var P=s[m],I=t[m];if(!a(P)||null===I||"object"!=typeof I&&"function"!=typeof I)Array.isArray(P)?(t[m]=[],l(t[m],P,!1)):a(P)?t[m]=o(P):t[m]=P;else{var L=u(P);Array.isArray(I)&&(1===L.length&&(L[0]===r.APPEND||L[0]===r.REMOVE)&&Array.isArray(P[L[0]])||2===L.length&&L.sort().join(",")===r.APPEND+","+r.REMOVE&&Array.isArray(P[r.APPEND])&&Array.isArray(P[r.REMOVE]))?(P[r.REMOVE]&&(I=t[m]=I.filter(function(j){return P[r.REMOVE].indexOf(j)<0})),P[r.APPEND]&&(t[m]=w(w([],E(I),!1),E(P[r.APPEND]),!1))):l(I,P,c)}};try{for(var b=M(u(s)),S=b.next();!S.done;S=b.next()){p(S.value)}}catch(m){h={error:m}}finally{try{S&&!S.done&&(d=b.return)&&d.call(b)}finally{if(h)throw h.error}}return t}function y(t){for(var s,c,h=[],d=1;d<arguments.length;d++)h[d-1]=arguments[d];var p={};try{for(var b=M(h),S=b.next();!S.done;S=b.next()){var A=S.value;t.hasOwnProperty(A)&&(p[A]=t[A])}}catch(m){s={error:m}}finally{try{S&&!S.done&&(c=b.return)&&c.call(b)}finally{if(s)throw s.error}}return p}r.Expandable=n,r.expandable=e,r.makeArray=function i(t){return Array.isArray(t)?t:[t]},r.keys=u,r.copy=o,r.insert=l,r.defaultOptions=function f(t){for(var s=[],c=1;c<arguments.length;c++)s[c-1]=arguments[c];return s.forEach(function(h){return l(t,h,!1)}),t},r.userOptions=function v(t){for(var s=[],c=1;c<arguments.length;c++)s[c-1]=arguments[c];return s.forEach(function(h){return l(t,h,!0)}),t},r.selectOptions=y,r.selectOptionsFromKeys=function g(t,s){return y.apply(void 0,w([t],E(Object.keys(s)),!1))},r.separateOptions=function O(t){for(var s,c,h,d,p=[],b=1;b<arguments.length;b++)p[b-1]=arguments[b];var S=[];try{for(var A=M(p),m=A.next();!m.done;m=A.next()){var P=m.value,I={},L={};try{for(var j=(h=void 0,M(Object.keys(t||{}))),R=j.next();!R.done;R=j.next()){var C=R.value;(void 0===P[C]?L:I)[C]=t[C]}}catch(D){h={error:D}}finally{try{R&&!R.done&&(d=j.return)&&d.call(j)}finally{if(h)throw h.error}}S.push(I),t=L}}catch(D){s={error:D}}finally{try{m&&!m.done&&(c=A.return)&&c.call(A)}finally{if(s)throw s.error}}return S.unshift(t),S},r.lookup=function _(t,s,c){return void 0===c&&(c=null),s.hasOwnProperty(t)?s[t]:c}},21108:(N,r)=>{Object.defineProperty(r,"__esModule",{value:!0}),r.px=r.emRounded=r.em=r.percent=r.length2em=r.MATHSPACE=r.RELUNITS=r.UNITS=r.BIGDIMEN=void 0,r.BIGDIMEN=1e6,r.UNITS={px:1,in:96,cm:96/2.54,mm:96/25.4},r.RELUNITS={em:1,ex:.431,pt:.1,pc:1.2,mu:1/18},r.MATHSPACE={veryverythinmathspace:1/18,verythinmathspace:2/18,thinmathspace:3/18,mediummathspace:4/18,thickmathspace:5/18,verythickmathspace:6/18,veryverythickmathspace:7/18,negativeveryverythinmathspace:-1/18,negativeverythinmathspace:-2/18,negativethinmathspace:-3/18,negativemediummathspace:-4/18,negativethickmathspace:-5/18,negativeverythickmathspace:-6/18,negativeveryverythickmathspace:-7/18,thin:.04,medium:.06,thick:.1,normal:1,big:2,small:1/Math.sqrt(2),infinity:r.BIGDIMEN},r.length2em=function M(n,e,i,u){if(void 0===e&&(e=0),void 0===i&&(i=1),void 0===u&&(u=16),"string"!=typeof n&&(n=String(n)),""===n||null==n)return e;if(r.MATHSPACE[n])return r.MATHSPACE[n];var o=n.match(/^\s*([-+]?(?:\.\d+|\d+(?:\.\d*)?))?(pt|em|ex|mu|px|pc|in|mm|cm|%)?/);if(!o)return e;var l=parseFloat(o[1]||"1"),f=o[2];return r.UNITS.hasOwnProperty(f)?l*r.UNITS[f]/u/i:r.RELUNITS.hasOwnProperty(f)?l*r.RELUNITS[f]:"%"===f?l/100*e:l*e},r.percent=function E(n){return(100*n).toFixed(1).replace(/\.?0+$/,"")+"%"},r.em=function w(n){return Math.abs(n)<.001?"0":n.toFixed(3).replace(/\.?0+$/,"")+"em"},r.emRounded=function T(n,e){return void 0===e&&(e=16),n=(Math.round(n*e)+.05)/e,Math.abs(n)<.001?"0em":n.toFixed(3).replace(/\.?0+$/,"")+"em"},r.px=function a(n,e,i){return void 0===e&&(e=-r.BIGDIMEN),void 0===i&&(i=16),n*=i,e&&n<e&&(n=e),Math.abs(n)<.1?"0":n.toFixed(1).replace(/\.0$/,"")+"px"}}}]);