(window.webpackJsonp=window.webpackJsonp||[]).push([[50],{149:function(e,t,r){"use strict";r.r(t),r.d(t,"frontMatter",(function(){return i})),r.d(t,"metadata",(function(){return c})),r.d(t,"rightToc",(function(){return s})),r.d(t,"default",(function(){return l}));var n=r(1),a=r(6),o=(r(0),r(156)),i={id:"security",title:"Encryption",sidebar_label:"Encryption"},c={id:"security",title:"Encryption",description:"# Privacy at the Core",source:"@site/docs/security.md",permalink:"/ODESI/docs/security",editUrl:"https://github.com/Open-Orchard/ODESI/edit/master/website/docs/security.md",sidebar_label:"Encryption",sidebar:"someSidebar",previous:{title:"About OpenSeed",permalink:"/ODESI/docs/about"},next:{title:"Getting Started",permalink:"/ODESI/docs/getstarted"}},s=[],p={rightToc:s};function l(e){var t=e.components,r=Object(a.a)(e,["components"]);return Object(o.b)("wrapper",Object(n.a)({},p,r,{components:t,mdxType:"MDXLayout"}),Object(o.b)("h1",{id:"privacy-at-the-core"},"Privacy at the Core"),Object(o.b)("p",null,"At the base of every OpenSeed service is the concept of privacy at every level. Chats are encrypted using a key that is only known by the recipients of the chat. Applications are required to encrypt all data from their app to OpenSeed and should expect encrypted data to be returned from the server. Applications can store information on OpenSeed that is encrypted to protect trade secrets or to limit exposure when dealing with sensitive information. "),Object(o.b)("p",null,"This is done by what we call encapsulated encryption. This method requires each transaction to contain at least 2 separate encryption keys for any transaction. Though a more detailed info-graphic is needed here is a very rough idea on how it works."),Object(o.b)("ul",null,Object(o.b)("li",{parentName:"ul"},"For user data (profiles, location, settings, etc.):  { app-key { user-key { data }}}"),Object(o.b)("li",{parentName:"ul"},"For app data (news, updates, etc.):  { dev-key { app-key { data }}}"),Object(o.b)("li",{parentName:"ul"},"For chat data:  { app-key { user-key { chat-key { data }}}")),Object(o.b)("h1",{id:"base-line-encryption"},"Base Line Encryption"),Object(o.b)("p",null,"OpenSeed is designed to work with as many tool-kits and sdks as possible as such we have to find a balance between security and our goal to break down silos between applications at the core level. As such, we have a simple encryption algorithm that is distributed with the OpenSeed libraries. We will continue to improve on this as time goes on to ensure security and privacy for everyone involved. "),Object(o.b)("h1",{id:"disclaimer"},"Disclaimer"),Object(o.b)("p",null,"No encryption is perfect, and OpenSeed is not responsible for applications or developers that misuse the system in a way that compromises privacy or security. We will require the use of BLE for any application on our system and developers will have to sign an agreement stating that they will adhere to these practices or face termination of service. "))}l.isMDXComponent=!0},156:function(e,t,r){"use strict";r.d(t,"a",(function(){return u})),r.d(t,"b",(function(){return b}));var n=r(0),a=r.n(n);function o(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function c(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){o(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var p=a.a.createContext({}),l=function(e){var t=a.a.useContext(p),r=t;return e&&(r="function"==typeof e?e(t):c({},t,{},e)),r},u=function(e){var t=l(e.components);return a.a.createElement(p.Provider,{value:t},e.children)},d={inlineCode:"code",wrapper:function(e){var t=e.children;return a.a.createElement(a.a.Fragment,{},t)}},y=Object(n.forwardRef)((function(e,t){var r=e.components,n=e.mdxType,o=e.originalType,i=e.parentName,p=s(e,["components","mdxType","originalType","parentName"]),u=l(r),y=n,b=u["".concat(i,".").concat(y)]||u[y]||d[y]||o;return r?a.a.createElement(b,c({ref:t},p,{components:r})):a.a.createElement(b,c({ref:t},p))}));function b(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var o=r.length,i=new Array(o);i[0]=y;var c={};for(var s in t)hasOwnProperty.call(t,s)&&(c[s]=t[s]);c.originalType=e,c.mdxType="string"==typeof e?e:n,i[1]=c;for(var p=2;p<o;p++)i[p]=r[p];return a.a.createElement.apply(null,i)}return a.a.createElement.apply(null,r)}y.displayName="MDXCreateElement"}}]);