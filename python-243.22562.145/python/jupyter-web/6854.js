"use strict";(self.webpackChunkjupyter_web=self.webpackChunkjupyter_web||[]).push([[6854],{76854:(w,n,c)=>{c.r(n),c.d(n,{rpmChanges:()=>t,rpmSpec:()=>g});var a=/^-+$/,o=/^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)  ?\d{1,2} \d{2}:\d{2}(:\d{2})? [A-Z]{3,4} \d{4} - /,i=/^[\w+.-]+@[\w.-]+/;const t={name:"rpmchanges",token:function(r){return r.sol()&&(r.match(a)||r.match(o))?"tag":r.match(i)?"string":(r.next(),null)}};var l=/^(i386|i586|i686|x86_64|ppc64le|ppc64|ppc|ia64|s390x|s390|sparc64|sparcv9|sparc|noarch|alphaev6|alpha|hppa|mipsel)/,p=/^[a-zA-Z0-9()]+:/,u=/^%(debug_package|package|description|prep|build|install|files|clean|changelog|preinstall|preun|postinstall|postun|pretrans|posttrans|pre|post|triggerin|triggerun|verifyscript|check|triggerpostun|triggerprein|trigger)/,f=/^%(ifnarch|ifarch|if)/,h=/^%(else|endif)/,d=/^(\!|\?|\<\=|\<|\>\=|\>|\=\=|\&\&|\|\|)/;const g={name:"rpmspec",startState:function(){return{controlFlow:!1,macroParameters:!1,section:!1}},token:function(r,e){if("#"==r.peek())return r.skipToEnd(),"comment";if(r.sol()){if(r.match(p))return"header";if(r.match(u))return"atom"}if(r.match(/^\$\w+/)||r.match(/^\$\{\w+\}/))return"def";if(r.match(h))return"keyword";if(r.match(f))return e.controlFlow=!0,"keyword";if(e.controlFlow){if(r.match(d))return"operator";if(r.match(/^(\d+)/))return"number";r.eol()&&(e.controlFlow=!1)}if(r.match(l))return r.eol()&&(e.controlFlow=!1),"number";if(r.match(/^%[\w]+/))return r.match("(")&&(e.macroParameters=!0),"keyword";if(e.macroParameters){if(r.match(/^\d+/))return"number";if(r.match(")"))return e.macroParameters=!1,"keyword"}return r.match(/^%\{\??[\w \-\:\!]+\}/)?(r.eol()&&(e.controlFlow=!1),"def"):(r.next(),null)}}}}]);