# JavaScript

## 描述：

首先它是轻量级脚本语言。

不具备开发操作系统的能力，用来编写控制大型系统的脚本。

嵌入大型系统，调用大型系统提供的API。

最常见的宿主环境为**浏览器**和**服务器环境**（Node 项目）。

**浏览器API：**

- 浏览器控制类：操作浏览器
- DOM类：操作网页的各种元素
- Web类：实现互联网的各种功能

**服务器：**

- 文件操作API
- 网络通信API等

## 变量：

### 声明与赋值

变量是对“值”的具名引用。

`var i = 1;`

声明一个变量，`i`是变量名，保存的是`1`在内存中的地址。

当访问`1`时，首先是根据`i`所存储的变量地址，去内存中访问该地址对应的值。

### 变量提升（函数也会提升）

JavaScript 引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升（hoisting）

```javascript
console.log(a)
var a = 1;
```

变量提升后如下：

```js
var a;
console.log(a);
a = 1;
```

控制台不会报错，但是打印的是`undefined`。

## 标识符与保留字

### 标识符命名

驼峰命名法（大驼峰小驼峰）

匈牙利命名法

下划线命名法

目的：增强程序的可读性。

## 标签（label）

```js
label:
	语句
```

标签可以是任意的标识符，但不能是保留字，语句部分可以是任意语句。

标签通常与`break`语句和`continue`语句配合使用，跳出特定的循环。

不要试图记住，`break label`、`continue label`是跳出哪层循环。

理解`break`、`continue`的作用。

```js
break      ====>   label 		break 	 （跳出）该标签
continue   ====>   label		continue （继续）该标签
```

## 数据类型（6种）

`ES6` 又新增了第七种 Symbol 类型的值。

- 数值（number）：整数和小数（比如`1`和`3.14`）
- 字符串（string）：文本（比如`Hello World`）。
- 布尔值（boolean）：表示真伪的两个特殊值，即`true`（真）和`false`（假）
- `undefined`：表示“未定义”或不存在，即由于目前没有定义，所以此处暂时没有任何值
- `null`：表示空值，即此处的值为空。
- 对象（object）：各种值组成的集合。

### null 与 undefined

```js
Number(null)		//表示为空的对象
//0
Number(undefined)	//此处无定义
//NaN
```

### 原始类型：

数值、布尔、字符串

### 精度：

由于计算机存储二进制浮点数的表示导致的，其他语言有decimal库来规避，而JavaScript没有。一般处理办法，将浮点数转化为整数计算后再转化为浮点数。

```js
0.1+0.2
0.30000000000000004
```

### 判断类型：

- `typeof`运算符
- `instanceof`运算符
- `Object.prototype.toString`方法

```js
a = 1
typeof a
//"number"
typeof null
//"object"   历史原因
typeof undefined
//"undefined"
```

### 布尔：

判假：

- `undefined`
- `null`
- `false`
- `0`
- `NaN`
- `""`或`''`（空字符串）

空数组和空对象都为`true`。

```js
if([])
    console.log('true')
//true
if({})
    console.log('true')
//true
```

### 0

JavaScript 内部实际上存在2个`0`：一个是`+0`，一个是`-0`，区别就是64位浮点数表示法的符号位不同。它们是等价的。

```
-0 === +0 // true
0 === -0 // true
0 === +0 // true
(1 / +0) === (1 / -0) // false
```

除以正零得到`+Infinity`，除以负零得到`-Infinity`，这两者是不相等的。

```js
1/+0
//Infinity 正无穷
1/-0
//-Infinity	负无穷
0/0
//NaN
```

### NaN

`NaN`是 JavaScript 的特殊值，表示“非数字”（Not a Number），是一特殊值，主要出现在将字符串解析成数字出错的场合。

```js
typeof NaN
//"number"
NaN === NaN
//false
```

`NaN`与任何数运算结果都为`NaN`。

switch和数组使用严格相等

## 字符串：

输出多行字符串：

```js
(function () { /*
line 1
line 2
line 3
*/}).toString().split('\n').slice(1, -1).join('\n')
// "line 1
// line 2
// line 3"
```

字符串可以被视为字符数组。

每个字符在 JavaScript 内部都是以16位（即2个字节）的 UTF-16 格式储存。

对于码点在`U+10000`到`U+10FFFF`之间的字符，JavaScript 总是认为它们是两个字符（`length`属性为2）。所以处理的时候，必须把这一点考虑在内，也就是说，JavaScript 返回的字符串长度可能是不正确的。

```js
'𝌆'.length
//2
```

