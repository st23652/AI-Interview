"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[525],{60525:(k,u,o)=>{o.r(u),o.d(u,{smalltalk:()=>v});var s=/[+\-\/\\*~<>=@%|&?!.,:;^]/,w=/true|false|nil|self|super|thisContext/,l=function(e,n){this.next=e,this.parent=n},r=function(e,n,t){this.name=e,this.context=n,this.eos=t},f=function(){this.context=new l(c,null),this.expectVariable=!0,this.indentation=0,this.userIndentationDelta=0};f.prototype.userIndent=function(e,n){this.userIndentationDelta=e>0?e/n-this.indentation:0};var c=function(e,n,t){var i=new r(null,n,!1),a=e.next();return'"'===a?i=h(e,new l(h,n)):"'"===a?i=p(e,new l(p,n)):"#"===a?"'"===e.peek()?(e.next(),i=d(e,new l(d,n))):e.eatWhile(/[^\s.{}\[\]()]/)?i.name="string.special":i.name="meta":"$"===a?("<"===e.next()&&(e.eatWhile(/[^\s>]/),e.next()),i.name="string.special"):"|"===a&&t.expectVariable?i.context=new l(x,n):/[\[\]{}()]/.test(a)?(i.name="bracket",i.eos=/[\[{(]/.test(a),"["===a?t.indentation++:"]"===a&&(t.indentation=Math.max(0,t.indentation-1))):s.test(a)?(e.eatWhile(s),i.name="operator",i.eos=";"!==a):/\d/.test(a)?(e.eatWhile(/[\w\d]/),i.name="number"):/[\w_]/.test(a)?(e.eatWhile(/[\w\d_]/),i.name=t.expectVariable?w.test(e.current())?"keyword":"variable":null):i.eos=t.expectVariable,i},h=function(e,n){return e.eatWhile(/[^"]/),new r("comment",e.eat('"')?n.parent:n,!0)},p=function(e,n){return e.eatWhile(/[^']/),new r("string",e.eat("'")?n.parent:n,!1)},d=function(e,n){return e.eatWhile(/[^']/),new r("string.special",e.eat("'")?n.parent:n,!1)},x=function(e,n){var t=new r(null,n,!1);return"|"===e.next()?(t.context=n.parent,t.eos=!0):(e.eatWhile(/[^|]/),t.name="variable"),t};const v={name:"smalltalk",startState:function(){return new f},token:function(e,n){if(n.userIndent(e.indentation(),e.indentUnit),e.eatSpace())return null;var t=n.context.next(e,n.context,n);return n.context=t.context,n.expectVariable=t.eos,t.name},blankLine:function(e,n){e.userIndent(0,n)},indent:function(e,n,t){var i=e.context.next===c&&n&&"]"===n.charAt(0)?-1:e.userIndentationDelta;return(e.indentation+i)*t.unit},languageData:{indentOnInput:/^\s*\]$/}}}}]);