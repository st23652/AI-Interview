"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[2958],{20089:(_,h,O)=>{Object.defineProperty(h,"__esModule",{value:!0}),h.AbstractFindMath=void 0;var P=O(80084),A=function(){function g(i){var T=this.constructor;this.options=(0,P.userOptions)((0,P.defaultOptions)({},T.OPTIONS),i)}return g.OPTIONS={},g}();h.AbstractFindMath=A},5520:(_,h)=>{Object.defineProperty(h,"__esModule",{value:!0}),h.newState=h.STATE=h.AbstractMathItem=h.protoItem=void 0,h.protoItem=function O(g,i,T,v,S,p,l){return void 0===l&&(l=null),{open:g,math:i,close:T,n:v,start:{n:S},end:{n:p},display:l}};var P=function(){function g(i,T,v,S,p){void 0===v&&(v=!0),void 0===S&&(S={i:0,n:0,delim:""}),void 0===p&&(p={i:0,n:0,delim:""}),this.root=null,this.typesetRoot=null,this.metrics={},this.inputData={},this.outputData={},this._state=h.STATE.UNPROCESSED,this.math=i,this.inputJax=T,this.display=v,this.start=S,this.end=p,this.root=null,this.typesetRoot=null,this.metrics={},this.inputData={},this.outputData={}}return Object.defineProperty(g.prototype,"isEscaped",{get:function(){return null===this.display},enumerable:!1,configurable:!0}),g.prototype.render=function(i){i.renderActions.renderMath(this,i)},g.prototype.rerender=function(i,T){void 0===T&&(T=h.STATE.RERENDER),this.state()>=T&&this.state(T-1),i.renderActions.renderMath(this,i,T)},g.prototype.convert=function(i,T){void 0===T&&(T=h.STATE.LAST),i.renderActions.renderConvert(this,i,T)},g.prototype.compile=function(i){this.state()<h.STATE.COMPILED&&(this.root=this.inputJax.compile(this,i),this.state(h.STATE.COMPILED))},g.prototype.typeset=function(i){this.state()<h.STATE.TYPESET&&(this.typesetRoot=i.outputJax[this.isEscaped?"escaped":"typeset"](this,i),this.state(h.STATE.TYPESET))},g.prototype.updateDocument=function(i){},g.prototype.removeFromDocument=function(i){void 0===i&&(i=!1)},g.prototype.setMetrics=function(i,T,v,S,p){this.metrics={em:i,ex:T,containerWidth:v,lineWidth:S,scale:p}},g.prototype.state=function(i,T){return void 0===i&&(i=null),void 0===T&&(T=!1),null!=i&&(i<h.STATE.INSERTED&&this._state>=h.STATE.INSERTED&&this.removeFromDocument(T),i<h.STATE.TYPESET&&this._state>=h.STATE.TYPESET&&(this.outputData={}),i<h.STATE.COMPILED&&this._state>=h.STATE.COMPILED&&(this.inputData={}),this._state=i),this._state},g.prototype.reset=function(i){void 0===i&&(i=!1),this.state(h.STATE.UNPROCESSED,i)},g}();h.AbstractMathItem=P,h.STATE={UNPROCESSED:0,FINDMATH:10,COMPILED:20,CONVERT:100,METRICS:110,RERENDER:125,TYPESET:150,INSERTED:200,LAST:1e4},h.newState=function A(g,i){if(g in h.STATE)throw Error("State "+g+" already exists");h.STATE[g]=i}},92958:function(_,h,O){var f,P=this&&this.__extends||(f=function(r,e){return(f=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,u){t.__proto__=u}||function(t,u){for(var o in u)Object.prototype.hasOwnProperty.call(u,o)&&(t[o]=u[o])})(r,e)},function(r,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function t(){this.constructor=r}f(r,e),r.prototype=null===e?Object.create(e):(t.prototype=e.prototype,new t)}),A=this&&this.__assign||function(){return A=Object.assign||function(f){for(var r,e=1,t=arguments.length;e<t;e++)for(var u in r=arguments[e])Object.prototype.hasOwnProperty.call(r,u)&&(f[u]=r[u]);return f},A.apply(this,arguments)},g=this&&this.__read||function(f,r){var e="function"==typeof Symbol&&f[Symbol.iterator];if(!e)return f;var u,E,t=e.call(f),o=[];try{for(;(void 0===r||r-- >0)&&!(u=t.next()).done;)o.push(u.value)}catch(b){E={error:b}}finally{try{u&&!u.done&&(e=t.return)&&e.call(t)}finally{if(E)throw E.error}}return o},i=this&&this.__importDefault||function(f){return f&&f.__esModule?f:{default:f}};Object.defineProperty(h,"__esModule",{value:!0}),h.TeX=void 0;var T=O(19380),v=O(80084),S=O(94718),p=i(O(8433)),l=i(O(60909)),c=i(O(55571)),a=i(O(6257)),n=i(O(46708)),s=O(22450),d=O(8890);O(80677);var y=function(f){function r(e){void 0===e&&(e={});var t=this,u=g((0,v.separateOptions)(e,r.OPTIONS,S.FindTeX.OPTIONS),3),o=u[0],E=u[1],b=u[2];(t=f.call(this,E)||this).findTeX=t.options.FindTeX||new S.FindTeX(b);var M=t.options.packages,I=t.configuration=r.configure(M),F=t._parseOptions=new n.default(I,[t.options,s.TagsFactory.OPTIONS]);return(0,v.userOptions)(F.options,o),I.config(t),r.tags(F,I),t.postFilters.add(p.default.cleanSubSup,-6),t.postFilters.add(p.default.setInherited,-5),t.postFilters.add(p.default.moveLimits,-4),t.postFilters.add(p.default.cleanStretchy,-3),t.postFilters.add(p.default.cleanAttributes,-2),t.postFilters.add(p.default.combineRelations,-1),t}return P(r,f),r.configure=function(e){var t=new d.ParserConfiguration(e,["tex"]);return t.init(),t},r.tags=function(e,t){s.TagsFactory.addTags(t.tags),s.TagsFactory.setDefault(e.options.tags),e.tags=s.TagsFactory.getDefault(),e.tags.configuration=e},r.prototype.setMmlFactory=function(e){f.prototype.setMmlFactory.call(this,e),this._parseOptions.nodeFactory.setMmlFactory(e)},Object.defineProperty(r.prototype,"parseOptions",{get:function(){return this._parseOptions},enumerable:!1,configurable:!0}),r.prototype.reset=function(e){void 0===e&&(e=0),this.parseOptions.tags.reset(e)},r.prototype.compile=function(e,t){this.parseOptions.clear(),this.executeFilters(this.preFilters,e,t,this.parseOptions);var o,E,u=e.display;this.latex=e.math,this.parseOptions.tags.startEquation(e);try{var b=new c.default(this.latex,{display:u,isInner:!1},this.parseOptions);o=b.mml(),E=b.stack.global}catch(M){if(!(M instanceof a.default))throw M;this.parseOptions.error=!0,o=this.options.formatError(this,M)}return o=this.parseOptions.nodeFactory.create("node","math",[o]),(null==E?void 0:E.indentalign)&&l.default.setAttribute(o,"indentalign",E.indentalign),u&&l.default.setAttribute(o,"display","block"),this.parseOptions.tags.finishEquation(e),this.parseOptions.root=o,this.executeFilters(this.postFilters,e,t,this.parseOptions),this.mathNode=this.parseOptions.root,this.mathNode},r.prototype.findMath=function(e){return this.findTeX.findMath(e)},r.prototype.formatError=function(e){var t=e.message.replace(/\n.*/,"");return this.parseOptions.nodeFactory.create("error",t,e.id,this.latex)},r.NAME="TeX",r.OPTIONS=A(A({},T.AbstractInputJax.OPTIONS),{FindTeX:null,packages:["base"],digits:/^(?:[0-9]+(?:\{,\}[0-9]{3})*(?:\.[0-9]*)?|\.[0-9]+)/,maxBuffer:5120,formatError:function(e,t){return e.formatError(t)}}),r}(T.AbstractInputJax);h.TeX=y},8433:function(_,h,O){var P=this&&this.__values||function(v){var S="function"==typeof Symbol&&Symbol.iterator,p=S&&v[S],l=0;if(p)return p.call(v);if(v&&"number"==typeof v.length)return{next:function(){return v&&l>=v.length&&(v=void 0),{value:v&&v[l++],done:!v}}};throw new TypeError(S?"Object is not iterable.":"Symbol.iterator is not defined.")},A=this&&this.__importDefault||function(v){return v&&v.__esModule?v:{default:v}};Object.defineProperty(h,"__esModule",{value:!0});var T,g=O(91585),i=A(O(60909));(function(v){v.cleanStretchy=function(a){var n,s,d=a.data;try{for(var y=P(d.getList("fixStretchy")),f=y.next();!f.done;f=y.next()){var r=f.value;if(i.default.getProperty(r,"fixStretchy")){var e=i.default.getForm(r);e&&e[3]&&e[3].stretchy&&i.default.setAttribute(r,"stretchy",!1);var t=r.parent;if(!(i.default.getTexClass(r)||e&&e[2])){var u=d.nodeFactory.create("node","TeXAtom",[r]);t.replaceChild(u,r),u.inheritAttributesFrom(r)}i.default.removeProperties(r,"fixStretchy")}}}catch(o){n={error:o}}finally{try{f&&!f.done&&(s=y.return)&&s.call(y)}finally{if(n)throw n.error}}},v.cleanAttributes=function(a){a.data.root.walkTree(function(s,d){var y,f,r=s.attributes;if(r){var e=new Set((r.get("mjx-keep-attrs")||"").split(/ /));delete r.getAllAttributes()["mjx-keep-attrs"];try{for(var t=P(r.getExplicitNames()),u=t.next();!u.done;u=t.next()){var o=u.value;!e.has(o)&&r.attributes[o]===s.attributes.getInherited(o)&&delete r.attributes[o]}}catch(E){y={error:E}}finally{try{u&&!u.done&&(f=t.return)&&f.call(t)}finally{if(y)throw y.error}}}},{})},v.combineRelations=function(a){var n,s,d,y,f=[];try{for(var r=P(a.data.getList("mo")),e=r.next();!e.done;e=r.next()){var t=e.value;if(!t.getProperty("relationsCombined")&&t.parent&&(!t.parent||i.default.isType(t.parent,"mrow"))&&i.default.getTexClass(t)===g.TEXCLASS.REL){for(var u=t.parent,o=void 0,E=u.childNodes,b=E.indexOf(t)+1,M=i.default.getProperty(t,"variantForm");b<E.length&&(o=E[b])&&i.default.isType(o,"mo")&&i.default.getTexClass(o)===g.TEXCLASS.REL;){if(M!==i.default.getProperty(o,"variantForm")||!p(t,o)){null==t.attributes.getExplicit("rspace")&&i.default.setAttribute(t,"rspace","0pt"),null==o.attributes.getExplicit("lspace")&&i.default.setAttribute(o,"lspace","0pt");break}i.default.appendChildren(t,i.default.getChildren(o)),S(["stretchy","rspace"],t,o);try{for(var I=(d=void 0,P(o.getPropertyNames())),F=I.next();!F.done;F=I.next()){var x=F.value;t.setProperty(x,o.getProperty(x))}}catch(j){d={error:j}}finally{try{F&&!F.done&&(y=I.return)&&y.call(I)}finally{if(d)throw d.error}}E.splice(b,1),f.push(o),o.parent=null,o.setProperty("relationsCombined",!0)}t.attributes.setInherited("form",t.getForms()[0])}}}catch(j){n={error:j}}finally{try{e&&!e.done&&(s=r.return)&&s.call(r)}finally{if(n)throw n.error}}a.data.removeFromList("mo",f)};var S=function(a,n,s){var d=n.attributes,y=s.attributes;a.forEach(function(f){var r=y.getExplicit(f);null!=r&&d.set(f,r)})},p=function(a,n){var s,d,y=function(b,M){return b.getExplicitNames().filter(function(F){return F!==M&&("stretchy"!==F||b.getExplicit("stretchy"))})},f=a.attributes,r=n.attributes,e=y(f,"lspace"),t=y(r,"rspace");if(e.length!==t.length)return!1;try{for(var u=P(e),o=u.next();!o.done;o=u.next()){var E=o.value;if(f.getExplicit(E)!==r.getExplicit(E))return!1}}catch(b){s={error:b}}finally{try{o&&!o.done&&(d=u.return)&&d.call(u)}finally{if(s)throw s.error}}return!0},l=function(a,n,s){var d,y,f=[];try{for(var r=P(a.getList("m"+n+s)),e=r.next();!e.done;e=r.next()){var t=e.value,u=t.childNodes;if(!u[t[n]]||!u[t[s]]){var o=t.parent,E=u[t[n]]?a.nodeFactory.create("node","m"+n,[u[t.base],u[t[n]]]):a.nodeFactory.create("node","m"+s,[u[t.base],u[t[s]]]);i.default.copyAttributes(t,E),o?o.replaceChild(E,t):a.root=E,f.push(t)}}}catch(b){d={error:b}}finally{try{e&&!e.done&&(y=r.return)&&y.call(r)}finally{if(d)throw d.error}}a.removeFromList("m"+n+s,f)};v.cleanSubSup=function(a){var n=a.data;n.error||(l(n,"sub","sup"),l(n,"under","over"))};var c=function(a,n,s){var d,y,f=[];try{for(var r=P(a.getList(n)),e=r.next();!e.done;e=r.next()){var t=e.value;if(!t.attributes.get("displaystyle")){var u=t.childNodes[t.base],o=u.coreMO();if(u.getProperty("movablelimits")&&!o.attributes.getExplicit("movablelimits")){var E=a.nodeFactory.create("node",s,t.childNodes);i.default.copyAttributes(t,E),t.parent?t.parent.replaceChild(E,t):a.root=E,f.push(t)}}}}catch(b){d={error:b}}finally{try{e&&!e.done&&(y=r.return)&&y.call(r)}finally{if(d)throw d.error}}a.removeFromList(n,f)};v.moveLimits=function(a){var n=a.data;c(n,"munderover","msubsup"),c(n,"munder","msub"),c(n,"mover","msup")},v.setInherited=function(a){a.data.root.setInheritedAttributes({},a.math.display,0,!1)}})(T||(T={})),h.default=T},94718:function(_,h,O){var S,P=this&&this.__extends||(S=function(p,l){return(S=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(c,a){c.__proto__=a}||function(c,a){for(var n in a)Object.prototype.hasOwnProperty.call(a,n)&&(c[n]=a[n])})(p,l)},function(p,l){if("function"!=typeof l&&null!==l)throw new TypeError("Class extends value "+String(l)+" is not a constructor or null");function c(){this.constructor=p}S(p,l),p.prototype=null===l?Object.create(l):(c.prototype=l.prototype,new c)}),A=this&&this.__read||function(S,p){var l="function"==typeof Symbol&&S[Symbol.iterator];if(!l)return S;var a,s,c=l.call(S),n=[];try{for(;(void 0===p||p-- >0)&&!(a=c.next()).done;)n.push(a.value)}catch(d){s={error:d}}finally{try{a&&!a.done&&(l=c.return)&&l.call(c)}finally{if(s)throw s.error}}return n};Object.defineProperty(h,"__esModule",{value:!0}),h.FindTeX=void 0;var g=O(20089),i=O(74267),T=O(5520),v=function(S){function p(l){var c=S.call(this,l)||this;return c.getPatterns(),c}return P(p,S),p.prototype.getPatterns=function(){var l=this,c=this.options,a=[],n=[],s=[];this.end={},this.env=this.sub=0;var d=1;c.inlineMath.forEach(function(y){return l.addPattern(a,y,!1)}),c.displayMath.forEach(function(y){return l.addPattern(a,y,!0)}),a.length&&n.push(a.sort(i.sortLength).join("|")),c.processEnvironments&&(n.push("\\\\begin\\s*\\{([^}]*)\\}"),this.env=d,d++),c.processEscapes&&s.push("\\\\([\\\\$])"),c.processRefs&&s.push("(\\\\(?:eq)?ref\\s*\\{[^}]*\\})"),s.length&&(n.push("("+s.join("|")+")"),this.sub=d),this.start=new RegExp(n.join("|"),"g"),this.hasPatterns=n.length>0},p.prototype.addPattern=function(l,c,a){var n=A(c,2),s=n[0],d=n[1];l.push((0,i.quotePattern)(s)),this.end[s]=[d,a,this.endPattern(d)]},p.prototype.endPattern=function(l,c){return new RegExp((c||(0,i.quotePattern)(l))+"|\\\\(?:[a-zA-Z]|.)|[{}]","g")},p.prototype.findEnd=function(l,c,a,n){for(var e,s=A(n,3),d=s[0],y=s[1],f=s[2],r=f.lastIndex=a.index+a[0].length,t=0;e=f.exec(l);){if((e[1]||e[0])===d&&0===t)return(0,T.protoItem)(a[0],l.substr(r,e.index-r),e[0],c,a.index,e.index+e[0].length,y);"{"===e[0]?t++:"}"===e[0]&&t&&t--}return null},p.prototype.findMathInString=function(l,c,a){var n,s;for(this.start.lastIndex=0;n=this.start.exec(a);){if(void 0!==n[this.env]&&this.env){var d="\\\\end\\s*(\\{"+(0,i.quotePattern)(n[this.env])+"\\})";(s=this.findEnd(a,c,n,["{"+n[this.env]+"}",!0,this.endPattern(null,d)]))&&(s.math=s.open+s.math+s.close,s.open=s.close="")}else if(void 0!==n[this.sub]&&this.sub){var y=n[this.sub];d=n.index+n[this.sub].length;s=2===y.length?(0,T.protoItem)("",y.substr(1),"",c,n.index,d):(0,T.protoItem)("",y,"",c,n.index,d,!1)}else s=this.findEnd(a,c,n,this.end[n[0]]);s&&(l.push(s),this.start.lastIndex=s.end.n)}},p.prototype.findMath=function(l){var c=[];if(this.hasPatterns)for(var a=0,n=l.length;a<n;a++)this.findMathInString(c,a,l[a]);return c},p.OPTIONS={inlineMath:[["\\(","\\)"]],displayMath:[["$$","$$"],["\\[","\\]"]],processEscapes:!0,processEnvironments:!0,processRefs:!0},p}(g.AbstractFindMath);h.FindTeX=v}}]);