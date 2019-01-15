#### 1.**常用库**

re、time、datetime、os、sys、logging、

#### 2.**assert 断言**

**python -oo 优化**

#### 3.**python3 -m pip 运行指定版本的pip**

#### 4.**转码**

> urllib.quote()

> cgi.escape()

#### 5.**\_\_all_\_** 

在模块级别暴露接口

如果在`__all__`里没有暴露的接口，便不能访问

#### 6.**repr**

#### 7. locals、global

#### **8.导包**

相对路径

绝对路径

#### 9.**遍历**

```python
l = [1,2,3,4,5]
for i,x in enumerate(l):
    index = l.index(x)
    n = l.pop(index)
    print(i, '==>',' n = ',n)
------------------------------------------------
0 ==>  n =  1
1 ==>  n =  3
2 ==>  n =  5
```

如下：从lista中pop出所有type为2的字典(实际项目中还要修改字典重新传入列表)

```python
lista = [{'type': 2,'method': 'aaa'},
         {'type': 2,'method': 'sss'},
         {'type': 1,'method': 'www'}]
for i,x in enumerate(lista):
    if x['type'] == 2:
        index = lista.index(x)
        n = lista.pop(index)
        print(n)
print(lista)
--------------------------------------------------
{'type': 2, 'method': 'aaa'}
[{'type': 2, 'method': 'sss'}, {'type': 1, 'method': 'www'}]
```

解决办法：

```python
from copy import deepcopy
lista = [{'type': 2,'method': 'aaa'},
         {'type': 2,'method': 'sss'},
         {'type': 1,'method': 'www'}]

listb = deepcopy(lista)
for i,x in enumerate(listb):
    if x['type'] == 2:
        index = lista.index(x)
        n = lista.pop(index)
        print(n)
print('lista:',lista)
----------------------------------------------------------
{'method': 'aaa', 'type': 2}
{'method': 'sss', 'type': 2}
lista: [{'method': 'www', 'type': 1}]
```

#### 10. 内存管理

Python在进行内存管理从三个方面进行：

**对象的引用计数机制**
Python内部使用引用计数，来保持追踪内存中的对象， 所有对象都有引用计数。

引用计数增加的情况：
一个对象分配一个新名称
将其放入一个容器中（如列表List，元组tuple和字典dict）
引用计数减少的情况：
使用del语句对 对象别名显示的销毁
引用超出作用域或被重新赋值
sys.getrefcount()函数可以获得对象的当前引用计数。多数情况下，引用计数比你猜测的要大的多，对于不可变数据（如数字和字符串），解释器会在程序的不同部分共享内存，以便节约内存。

**垃圾回收机制**
python中的垃圾回收是以引用计数为主，标记-清除和分代收集为辅。

引用计数：Python在内存中存储每个对象的引用计数，如果计数变成0，该对象就会消失，分配给该对象的内存就会释放出来。
标记-清除：一些容器对象，比如说list、dict、tuple、instance等可能会出现引用循环，对于这些循环，垃圾回收器会定时回收这些循环（对象之间通过引用（指针）连在一起，构成一个有向图，对象构成这个有向图的节点，而引用关系构成这个有向图的边）。
分代收集：Python把内存根据对象存活时间划分为三代，对象创建之后，垃圾回收器会分配它们所属的代。每个对象都会被分配一个代，而被分配更年轻的代是被优先处理的，因此越晚创建的对象越容易被回收。
**内存池机制**
python提供了对内存的垃圾收集机制，将不用的的内存放到内存池而不是返回给操作系统。

Pymalloc机制，为了加速Python的执行效率，Python引入了一个Pymalloc机制，用于管理对小块内存(小于256个bits的对象)的申请和释放。
malloc机制，对于大的对象（大于256bits），直接执行 new/malloc 的行为来申请新的内存空间；

私有内存池，对于Python对象，如整数，浮点数和list，都有其独立的私有内存池，对象间不共享他们的内存池。也就是说如果你分配又释放了大量的整数，用于缓存这些整数的内存就不能再分配给浮点数。