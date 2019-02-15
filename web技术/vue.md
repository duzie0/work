# Vue

**模块组织**

```shell
├── build                      // 构建相关  
├── config                     // 配置相关
├── src                        // 源代码
│   ├── api                    // 所有请求
│   ├── assets                 // 主题 字体等静态资源
│   ├── components             // 全局公用组件
│   ├── directive              // 全局指令
│   ├── filtres                // 全局 filter
│   ├── icons                  // 项目所有 svg icons
│   ├── lang                   // 国际化 language
│   ├── mock                   // 项目mock 模拟数据
│   ├── router                 // 路由
│   ├── store                  // 全局 store管理
│   ├── styles                 // 全局样式
│   ├── utils                  // 全局公用方法
│   ├── vendor                 // 公用vendor
│   ├── views                   // view
│   ├── App.vue                // 入口页面
│   ├── main.js                // 入口 加载组件 初始化等
│   └── permission.js          // 权限管理
├── static                     // 第三方不打包资源
│   └── Tinymce                // 富文本
├── .babelrc                   // babel-loader 配置
├── eslintrc.js                // eslint 配置项
├── .gitignore                 // git 忽略项
├── favicon.ico                // favicon图标
├── index.html                 // html模板
└── package.json               // package.json

```

## 简介

优点：

- 实现了MVVM(渐进式框架)，View的变化会自动更新到ViewModel，ViewModel的变化也会自动同步到View上显示。这种自动同步是因为ViewModel中的属性实现了Observer，当属性变更时都能触发对应的操作。
- 轻量级框架
- 双向数据绑定
- 指令
- 插件化

缺点：

- 不支持低版本浏览器

MVVM最大的优势是编写前端逻辑非常复杂的页面，尤其是需要大量DOM操作的逻辑，利用MVVM可以极大地简化前端页面的逻辑。

但是MVVM不是万能的，它的目的是为了解决复杂的前端逻辑。对于以展示逻辑为主的页面，例如，新闻，博客、文档等，*不能*使用MVVM展示数据，因为这些页面需要被搜索引擎索引，而搜索引擎无法获取使用MVVM并通过API加载的数据。

所以，需要SEO（Search Engine Optimization）的页面，不能使用MVVM展示数据。不需要SEO的页面，如果前端逻辑复杂，就适合使用MVVM展示数据，例如，工具类页面，复杂的表单页面，用户登录后才能操作的页面等等。

### 单项绑定：model值的引用

### 双向绑定：v-model

### 内置指令

| 指令      | 描述                                                   |
| --------- | ------------------------------------------------------ |
| v-bind    | 响应并更新DOM特性 可以替换为“:”                        |
| v-on      | 用于监听dom事件 可以替换成“@”                          |
| v-model   | 数据双向绑定                                           |
| v-show    | 条件渲染指令，修改元素的displayCSS属性                 |
| v-if      | 条件渲染指令，直接销毁和重建DOM                        |
| v-else    | 条件渲染指令                                           |
| v-for     | 循环指令                                               |
| v-else-if | 判断多层条件，必须跟v-if成对使用                       |
| v-text    | 更新元素的textContent                                  |
| v-html    | 更新元素的innerHTML                                    |
| v-pre     | 不需要表达式，加快整个项目编译速度                     |
| v-cloak   | 不需要表达式，这个指令保持在元素上直到关联实例结束编译 |
| v-once    | 不需要表达式，只渲染元素或组件一次，随后不会再渲染     |

### 赋值

Vue之所以能够监听Model状态的变化，是因为JavaScript语言本身提供了`Proxy`或者`Object.observe()`机制来监听对象状态的变化。但是，对于数组元素的赋值，却没有办法直接监听，因此，如果我们直接对数组元素赋值。

#### 静态赋值：

#### 动态赋值：v-bind

### 命名

事件名与prop名