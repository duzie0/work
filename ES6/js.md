# ES6

## 继承与原型链

**prototype：原型**

**constructor：建造者**

谈到继承时，JavaScript 只有一种结构：对象。每个实例对象（object ）都有一个私有属性（称之为__proto__）指向它的原型对象（**prototype**）。该原型对象也有一个自己的原型对象(__proto__) ，层层向上直到一个对象的原型对象为 `null`。根据定义，`null` 没有原型，并作为这个**原型链**中的最后一个环节。

### 继承

JavaScript没有类似其他语言的类方法，在JavaScript中任何函数都可以作为对象的属性。

函数的继承，和其他属性的继承没有区别。

当继承的函数被调用时，**this 指向的是当前继承的对象**，而不是继承的函数所在的原型对象。

```js
var o = {
  a: 2,
  m: function(){
    return this.a + 1;
  }
};

console.log(o.m()); // 3
// 当调用 o.m 时,'this'指向了o.

var p = Object.create(o);
// p是一个继承自 o 的对象

p.a = 4; // 创建 p 的自身属性 a
console.log(p.m()); // 5
// 调用 p.m 时, 'this'指向 p. 
// 又因为 p 继承 o 的 m 函数
// 此时的'this.a' 即 p.a，即 p 的自身属性 'a' 
```



### 原型链

对于JavaScript而言，`{a:1,b:2}`是一对象。

JavaScript对象有一条指向一个原型对象的链。

**声明一个函数：**

```js
let f = function(){
    this.a = 1;
    this.b = 2;
}
```

f的原型：

```js
f.prototype
{constructor: ƒ}
```

给f定义属性：

```js
f.prototype.b = 10;
f.prototype.c = 3;
f.prototype.d = 4;
```

此时，f的原型：

```js
f.prototype
{b: 10, c: 3, d: 4, constructor: ƒ}
```

此时存在一条这样的原型链：               

> {a: 1, b: 2} ==> {b: 10,  c: 3, d: 4} ==> Object.prototype ==> null

```js
let o = new f()
o.constructor
ƒ (){
    this.a = 1;
    this.b = 2;
}
```

o的构造者是f，a、b是o的属性。

当访问一个属性的时候，则沿着原型链寻找，直至原型链为null。

```js
o.a
1
o.b //不会是10
2
o.c
3
o.d
4
o.e
undefined
```

在原型链上查找属性比较耗时，对性能有副作用，这在性能要求苛刻的情况下很重要。另外，试图访问不存在的属性时会遍历整个原型链。