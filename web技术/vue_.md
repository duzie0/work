## **1.vue优缺点**

优点：    

a)MVVM的开发模式，从dom中解脱出来，双向数据绑定；

b)数据更新采用异步事件机制；

c)采用单向数据流；    

d)组件式开发；   

 e)采用虚拟dom    

f)支持模板和jsx两种开发模式；

g)可以进行服务端渲染；    

h)扩展性强，既可以向上又可以向下扩展

缺点：   

 a)不兼容IE8以下版本

b)生态圈不繁荣，开源社区不活跃；

## **2.什么是前端路由？**

由前端控制路由地址，在前端实现通过路由的形式加载对应的页面，不需要向后端发起请求，前端通过改变url地址，然后监听url地址的变化，开始新的url渲染，异步的形式前端路由的两种形式   hash模式，history模式，目前只有两种

hash:www.baidu.com/#aaa使用#作为url的hash值，#在之前的定义是锚点连接，改变不会像后端发起请求，也可以通hashchange事件监听到hash的改变history:html5新增的api

## 3.vue的内置指令有哪些

（1）V-bind：响应并更新DOM特性 可以替换为“:”

（2）V-on：用于监听dom事件 可以替换成“@”

（3）V-model：数据双向绑定

（4）V-show：条件渲染指令

（5）V-if：条件渲染指令

（6）V-else：条件渲染指令

（7）V-for：循环指令

（8）V-else-if：判断多层条件，必须跟v-if成对使用

（9）V-text：更新元素的textContent

（10）V-html：更新元素的innerHTML

（11）V-pre：不需要表达式，加快整个项目编译速度

（12）V-cloak：不需要表达式，这个指令保持在元素上直到关联实例结束编译

（13）V-once：不需要表达式，只渲染元素或组件一次，随后不会再渲染

## **4.Vue和SEO**

vue是一个开发框架，通过vue-router实现单页面应用的开发，单页面应用本身就对SEO不友好。

vue给出的官方解决方案：

vue-server-renderer服务端渲染，但是我觉得对于一个真正适合做成单页应用的项目的话，seo其实是可以不用考虑的，反正项目本身是需要登录才能进入的，但是像其他一些类似于商城的项目的话，我们可以吧项目分开，像单个的详情页我们没有必要放到单页路由中，可以把她们分出去，毕竟对于商城来说商品才是详情才是需要seo优化的。或者我们完全没有必要用了vue就得吧项目做成单页的，我们可以使用一些他的特性，毕竟我觉得vue给我带来最大的好处就是组件化开发；

**7.为什么使用路由懒加载**

也叫延迟加载，即在需要的时候进行加载，随用随载。因vue这种单页面应用，如果没有应用懒加载，运用webpack打包后的文件将会异常的大，造成进入首页时，需要加载的内容过多，时间过长，会出现长时间的白屏，即使做了loading也是不利于用户体验，而运用懒加载则可以将页面进行划分，需要的时候加载页面，可以有效的分担首页所承担的加载压力，减少首页加载用时懒加载形如下：importVuefrom'vue'importRouterfrom'vue-router'exportdefaultnewRouter({routes: [    {path:'/',name:'Index',component:resolve=>require('@/components/index',resolve),children:[        {path:'/index/indexs',name:'Indexs',component:resolve=>require('@/components/views/index/indexs',resolve)        }      ]    }  ]})

**8.什么是跨域**

跨域是指一个域下的文档或脚本视图去请求另一个域下的资源，这里跨域是广义的

**9.什么是同源策略？**

协议+域名+端口三者相同，即便两个不同的域名指向同一个ip地址，也非同源（只存在于客户端（浏览器））

**10.跨域解决方案**

（1）cors(跨域资源共享)（2）jsonp（3）iframe（4）nginx代理跨域（5）nodejs中间件代理跨域（6）WebSocket协议跨域

**11.jsonp的实现原理**

jsonp就是利用了请求js不涉及跨域的特性，以及js是浏览器脚本语言的特性，动态生成script标签，指定url为接口地址，并且创建一个不会冲突的函数添加到window上，前端通过query参数将回调函数的名称传递到后端，后端获取到名字，返回的内容就会执行js的形式返回方法名（数据）

缺点：只能是get请求，不能是post

不安全

需要后端配合

**12.cors跨域资源共享**

cors浏览器新增的跨域解决方案，需要客户端和服务端同时支持

客户端：（浏览器版本）

服务端：

//设置跨域访问

app.all('*', function(req, res, next) {     res.header("Access-Control-Allow-Origin","*"); //允许跨域访问的网站     res.header("Access-Control-Allow-Headers","X-Requested-With");//允许的headers字段         res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");//允许的请求方法       res.header("Access-Control-Allow-Crdentials",true)//允许携带cookie       res.header("Content-Type","application/json;charset=utf-8");  //接受到的内容格式     next();  });

优点：前端不需要做任何改变，只需要后端配置即可

 可以限制域名做请求

 可以跨域操作cookie

缺点：兼容性问题

**13.代理跨域（反向代理，正向代理）**

首先跨域问题是出现在浏览器同源策略，所以在服务端做一个代理，将不同域名下的数据请求，然后在通过当前服务器返回到当前页面

如：

proxyTable: {'/api': {'target':'http://localhost:3000/api','pathRewrite': {"^/api":""} //后面可以使重写的新路径，一般不做更改  }}

在脚手架config文件夹index.js文件有proxyTable对象

**14.开发环境和生产环境的区别**

日常开发工作中，一般会有两套构建环境：一套是在开发时用，构建结果用于本地开发调试，不进行代码压缩，打印debug信息，包含sourcemap文件；另一套构建后的结果是直接应用到线上的，代码要进行压缩，运行不打印debug信息，静态文件不包括sourcema。有时还要多出一套测试环境，在运行时直接进行请求mock等工作。

webpack 4.x版本在webpack配置中有mode选项可以直接配置production 或 development

webpack 3.x 一般是通过node命令传递环境变量，来控制不同环境下的构建行为

如：

{"scripts": {"build":"NODE_ENV=production webpack","dev":"NODE_ENV=development webpack-dev-server"}}

然后在 webpack.config.js 文件中可以通过 process.env.NODE_ENV 来获取命令传入的环境变量：

**常见的环境差异配置**

生产环境可能需要分离 CSS 成单独的文件，以便多个页面共享同一个 CSS 文件

生产环境需要压缩 HTML/CSS/JS 代码

生产环境需要压缩图片

开发环境需要生成 sourcemap 文件

开发环境需要打印 debug 信息

开发环境需要 live reload 或者 hot reload 的功能

以上是常见的构建环境需求差异，可能更加复杂的项目中会有更多的构建需求（如划分静态域名等），但是我们都可以通过判断环境变量来实现这些有环境差异的构建需求。

webpack 4.x 的 mode 已经提供了上述差异配置的大部分功能，mode 为 production 时默认使用 JS 代码压缩，而 mode 为 development 时默认启用 hot reload，等等。这样让我们的配置更为简洁，我们只需要针对特别使用的 loader 和 plugin 做区分配置就可以了。

webpack 3.x 版本还是只能自己动手修改配置来满足大部分环境差异需求。

**15.组件命名的约定**

Vue 2.0 中组件的命名限制与 1.0 的最大区别在于区分了大小写。总结一下就是：一是不使用非法的标签字符；二是不与 HTML 元素（区分大小写）或 SVG 元素（不区分大小写）重名；三是不使用 Vue 保留的 slot 和 component（区分大小写）。

除了以上三条，由于 Vue 2.0 内置了 KeepAlive、Transition、TransitionGroup 三个组件，所以尽量避免与这三个组件重名。但从另一方面讲，你也可以故意重名来实现一些特殊的功能。例如，keep-alive 的匹配顺序为 keep-alive、keepAlive、KeepAlive，所以我们可以注册一个 keep-alive 组件来拦截 KeepAlive 匹配。

建议：全小写或首字母大写

**16.vue的虚拟dom**

虚拟的DOM的核心思想是：对复杂的文档DOM结构，提供一种方便的工具，进行最小化地DOM操作。

**17.如何理解vue中MVVM模式？**

MVVM全称是Model-View-ViewModel；vue是以数据为驱动的，一旦创建dom和数据就保持同步，每当数据发生变化时，dom也会变化。DOMListeners和DataBindings是实现双向绑定的关键。DOMListeners监听页面所有View层DOM元素的变化，当发生变化，Model层的数据随之变化；DataBindings监听Model层的数据，当数据发生变化，View层的DOM元素随之变化。

**18.组件之间的传值通信**

**父组件向子组件传值：**

1）子组件在props中创建一个属性，用来接收父组件传过来的值；2）在父组件中注册子组件；3）在子组件标签中添加子组件props中创建的属性；4）把需要传给子组件的值赋给该属性

**子组件向父组件传值：**

1）子组件中需要以某种方式（如点击事件）的方法来触发一个自定义的事件；2）将需要传的值作为$emit的第二个参数，该值将作为实参传给响应事件的方法；3）在父组件中注册子组件并在子组件标签上绑定自定义事件的监听。

**19.scss是什么？在vue.cli中的安装使用步骤是？有哪几大特性？**

css的预编译；

**使用步骤：**

第一步：用npm 下三个loader（sass-loader、css-loader、node-sass）

第二步：在build目录找到webpack.base.config.js，在那个extends属性中加一个拓展.scss

第三步：还是在同一个文件，配置一个module属性

第四步：然后在组件的style标签加上lang属性 ，例如：lang=”scss”

**有哪几大特性:**

1、可以用变量，例如（$变量名称=值）；

2、可以用混合器，例如（）

3、可以嵌套

**20.vuex有哪几种属性？**

有五种，分别是 State、 Getter、Mutation 、Action、 Module

**21.vuex的State特性是？**

一、Vuex就是一个仓库，仓库里面放了很多对象。其中state就是数据源存放地，对应于与一般Vue对象里面的data

二、state里面存放的数据是响应式的，Vue组件从store中读取数据，若是store中的数据发生改变，依赖这个数据的组件也会发生更新

三、它通过mapState把全局的 state 和 getters 映射到当前组件的 computed 计算属性中

**22.vuex的Getter特性是？**

一、getters 可以对State进行计算操作，它就是Store的计算属性

二、 虽然在组件内也可以做计算属性，但是getters 可以在多组件之间复用

三、 如果一个状态只在一个组件内使用，是可以不用getters

**23.vuex的Mutation特性是？**

一、Action 类似于 mutation，不同在于：

二、Action 提交的是 mutation，而不是直接变更状态。

三、Action 可以包含任意异步操作

**24.Vue.js中ajax请求代码应该写在组件的methods中还是vuex的actions中？**

一、如果请求来的数据是不是要被其他组件公用，仅仅在请求的组件内使用，就不需要放入vuex 的state里。

二、如果被其他地方复用，这个很大几率上是需要的，如果需要，请将请求放入action里，方便复用，并包装成promise返回，在调用处用async await处理返回的数据。如果不要复用这个请求，那么直接写在vue文件里很方便。

**25.不用Vuex会带来什么问题？**

一、可维护性会下降，你要想修改数据，你得维护三个地方

二、可读性会下降，因为一个组件里的数据，你根本就看不出来是从哪来的

三、增加耦合，大量的上传派发，会让耦合性大大的增加，本来Vue用Component就是为了减少耦合，现在这么用，和组件化的初衷相背。

**26.axios的特点有哪些？**

（1）Axios 是一个基于 promise 的 HTTP 库，支持promise所有的API

（2）它可以拦截请求和响应

（3）它可以转换请求数据和响应数据，并对响应回来的内容自动转换成 JSON类型的数据

（4）安全性更高，客户端支持防御 XSRF

**27.axios有哪些常用方法？**

（1）axios.get(url[,config])//get请求用于列表和信息查询（2）axios.delete(url[,config])//删除（3）axios.post(url[, data[,config]])//post请求用于信息的添加（4）axios.put(url[, data[,config]])//更新操作

**28.说下你了解的axios相关配置属性？**

（1）url是用于请求的服务器URL

（2）method是创建请求时使用的方法,默认是get

（3）baseURL将自动加在url前面，除非url是一个绝对URL。它可以通过设置一个

（4）baseURL便于为axios实例的方法传递相对URL

（5）transformRequest允许在向服务器发送前，修改请求数据，只能用 

在'PUT','POST'和'PATCH'这几个请求方法

（6）headers是即将被发送的自定义请求头

（7）headers:{'X-Requested-With':'XMLHttpRequest'},

（8）params是即将与请求一起发送的URL参数，必须是一个无格式对象(plainobject)或URLSearchParams对象

params:{ID:12345},

（9）auth表示应该使用HTTP基础验证，并提供凭据

（10）这将设置一个Authorization头，覆写掉现有的任意使用headers设置的自定义Authorization头

auth:{username:'janedoe',    password:'s00pers3cret'},

（11）'proxy'定义代理服务器的主机名称和端口

`auth`表示HTTP基础验证应当用于连接代理，并提供凭据这将会设置一个`Proxy-Authorization`头，覆写掉已有的通过使用`header`设置的自定义   `Proxy-Authorization`头。

proxy:{    

​    host:'127.0.0.1',   

​     port:9000,    

​    auth::{        

​        username:'mikeymike',        

​        password:'rapunz3l'

​    }

},

**29.v-show和v-if指令的共同点和不同点?**

v-show指令是通过修改元素的displayCSS属性让其显示或者隐藏

v-if指令是直接销毁和重建DOM达到让元素显示和隐藏的效果