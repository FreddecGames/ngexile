import{u as P,d as B,c as y,h as N,r as w,o as z,a as I,b as j,e as L,f as U,g as C,i as E,j as T,p as V,k as H,n as D,l as F,m as q,q as M,w as O,s as $,t as G,v as Q,x as g,y as _,z as W,A as J,B as K,C as X,D as Y}from"./Cah09oso.js";import{u as Z}from"./DJd-sLOA.js";import{_ as ee}from"./DlAUqK2U.js";async function R(t,a=P()){const{path:l,matched:e}=a.resolve(t);if(!e.length||(a._routePreloaded||(a._routePreloaded=new Set),a._routePreloaded.has(l)))return;const n=a._preloadPromises=a._preloadPromises||[];if(n.length>4)return Promise.all(n).then(()=>R(t,a));a._routePreloaded.add(l);const s=e.map(c=>{var r;return(r=c.components)==null?void 0:r.default}).filter(c=>typeof c=="function");for(const c of s){const r=Promise.resolve(c()).catch(()=>{}).finally(()=>n.splice(n.indexOf(r)));n.push(r)}await Promise.all(n)}const te=(...t)=>t.find(a=>a!==void 0);function ae(t){const a=t.componentName||"NuxtLink";function l(e,n){if(!e||t.trailingSlash!=="append"&&t.trailingSlash!=="remove")return e;if(typeof e=="string")return k(e,t.trailingSlash);const s="path"in e&&e.path!==void 0?e.path:n(e).path;return{...e,name:void 0,path:k(s,t.trailingSlash)}}return B({name:a,props:{to:{type:[String,Object],default:void 0,required:!1},href:{type:[String,Object],default:void 0,required:!1},target:{type:String,default:void 0,required:!1},rel:{type:String,default:void 0,required:!1},noRel:{type:Boolean,default:void 0,required:!1},prefetch:{type:Boolean,default:void 0,required:!1},noPrefetch:{type:Boolean,default:void 0,required:!1},activeClass:{type:String,default:void 0,required:!1},exactActiveClass:{type:String,default:void 0,required:!1},prefetchedClass:{type:String,default:void 0,required:!1},replace:{type:Boolean,default:void 0,required:!1},ariaCurrentValue:{type:String,default:void 0,required:!1},external:{type:Boolean,default:void 0,required:!1},custom:{type:Boolean,default:void 0,required:!1}},setup(e,{slots:n}){const s=P(),c=F(),r=y(()=>{const o=e.to||e.href||"";return l(o,s.resolve)}),d=y(()=>typeof r.value=="string"&&N(r.value,{acceptRelative:!0})),p=y(()=>e.target&&e.target!=="_self"),x=y(()=>e.external||p.value?!0:typeof r.value=="object"?!1:r.value===""||d.value),S=w(!1),h=w(null),A=o=>{var f;h.value=e.custom?(f=o==null?void 0:o.$el)==null?void 0:f.nextElementSibling:o==null?void 0:o.$el};if(e.prefetch!==!1&&e.noPrefetch!==!0&&e.target!=="_blank"&&!oe()){const f=q();let v,i=null;z(()=>{const b=ne();I(()=>{v=j(()=>{var u;(u=h==null?void 0:h.value)!=null&&u.tagName&&(i=b.observe(h.value,async()=>{i==null||i(),i=null;const m=typeof r.value=="string"?r.value:s.resolve(r.value).fullPath;await Promise.all([f.hooks.callHook("link:prefetch",m).catch(()=>{}),!x.value&&R(r.value,s).catch(()=>{})]),S.value=!0}))})})}),L(()=>{v&&U(v),i==null||i(),i=null})}return()=>{var i,b;if(!x.value){const u={ref:A,to:r.value,activeClass:e.activeClass||t.activeClass,exactActiveClass:e.exactActiveClass||t.exactActiveClass,replace:e.replace,ariaCurrentValue:e.ariaCurrentValue,custom:e.custom};return e.custom||(S.value&&(u.class=e.prefetchedClass||t.prefetchedClass),u.rel=e.rel||void 0),C(E("RouterLink"),u,n.default)}const o=typeof r.value=="object"?((i=s.resolve(r.value))==null?void 0:i.href)??null:r.value&&!e.external&&!d.value?l(T(c.app.baseURL,r.value),s.resolve):r.value||null,f=e.target||null,v=te(e.noRel?"":e.rel,t.externalRelAttribute,d.value||p.value?"noopener noreferrer":"")||null;if(e.custom){if(!n.default)return null;const u=()=>M(o,{replace:e.replace,external:e.external});return n.default({href:o,navigate:u,get route(){if(!o)return;const m=V(o);return{path:m.pathname,fullPath:m.pathname,get query(){return H(m.search)},hash:m.hash,params:{},name:void 0,matched:[],redirectedFrom:void 0,meta:{},href:o}},rel:v,target:f,isExternal:x.value,isActive:!1,isExactActive:!1})}return C("a",{ref:h,href:o,rel:v,target:f},(b=n.default)==null?void 0:b.call(n))}}})}const re=ae(D);function k(t,a){const l=a==="append"?O:$;return N(t)&&!t.startsWith("http")?t:l(t,!0)}function ne(){const t=q();if(t._observer)return t._observer;let a=null;const l=new Map,e=(s,c)=>(a||(a=new IntersectionObserver(r=>{for(const d of r){const p=l.get(d.target);(d.isIntersecting||d.intersectionRatio>0)&&p&&p()}})),l.set(s,c),a.observe(s),()=>{l.delete(s),a.unobserve(s),l.size===0&&(a.disconnect(),a=null)});return t._observer={observe:e}}function oe(){const t=navigator.connection;return!!(t&&(t.saveData||/2g/.test(t.effectiveType)))}const se=t=>(X("data-v-ccd3db62"),t=t(),Y(),t),le={class:"font-sans antialiased bg-white dark:bg-black text-black dark:text-white grid min-h-screen place-content-center overflow-hidden"},ie=se(()=>g("div",{class:"fixed left-0 right-0 spotlight z-10"},null,-1)),ce={class:"max-w-520px text-center z-20"},ue=["textContent"],de=["textContent"],fe={class:"w-full flex items-center justify-center"},he={__name:"error-404",props:{appName:{type:String,default:"Nuxt"},version:{type:String,default:""},statusCode:{type:Number,default:404},statusMessage:{type:String,default:"Not Found"},description:{type:String,default:"Sorry, the page you are looking for could not be found."},backHome:{type:String,default:"Go back home"}},setup(t){const a=t;return Z({title:`${a.statusCode} - ${a.statusMessage} | ${a.appName}`,script:[],style:[{children:'*,:before,:after{-webkit-box-sizing:border-box;box-sizing:border-box;border-width:0;border-style:solid;border-color:#e0e0e0}*{--tw-ring-inset:var(--tw-empty, );--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgba(14, 165, 233, .5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000}:root{-moz-tab-size:4;-o-tab-size:4;tab-size:4}a{color:inherit;text-decoration:inherit}body{margin:0;font-family:inherit;line-height:inherit}html{-webkit-text-size-adjust:100%;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,"Apple Color Emoji","Segoe UI Emoji",Segoe UI Symbol,"Noto Color Emoji";line-height:1.5}h1,p{margin:0}h1{font-size:inherit;font-weight:inherit}'}]}),(l,e)=>{const n=re;return G(),Q("div",le,[ie,g("div",ce,[g("h1",{class:"text-8xl sm:text-10xl font-medium mb-8",textContent:_(t.statusCode)},null,8,ue),g("p",{class:"text-xl px-8 sm:px-0 sm:text-4xl font-light mb-16 leading-tight",textContent:_(t.description)},null,8,de),g("div",fe,[W(n,{to:"/",class:"gradient-border text-md sm:text-xl py-2 px-4 sm:py-3 sm:px-6 cursor-pointer"},{default:J(()=>[K(_(t.backHome),1)]),_:1})])])])}}},ge=ee(he,[["__scopeId","data-v-ccd3db62"]]);export{ge as default};
