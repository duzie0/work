# JavaScript

## 兼容性

|            | Chrome | IE   |
| ---------- | ------ | ---- |
| toFixed    |        |      |
| data-value |        |      |
|            |        |      |

## 1. data-value 的获取：

```html
<button type="button" data-type="upload">
    上传
</button>
```

|                   | dataset                      | getAttribute                             |
| ----------------- | ---------------------------- | ---------------------------------------- |
| **IE**            | 不支持                       | Query('button').getAttibute('data-type') |
| **Google Chrome** | Query('button').dataset.type | Query('button').getAttibute('data-type') |

## 2. window.onbeforeunload

```js
window.onbeforunload = function(){
    return '确定要刷新或退出吗？'
}
```

新版本的Google Chrome、火狐等不再支持自定义消息，IE还支持

## 3. _format 函数

```js
var _format = function(str,obj){
    var result = str;
    if(result.length > 0){
        if((typeof obj) == 'object'){
            for (var key in obj){
                if(obj[key] != undefined){
                    var reg = new RegExp("({"+key+"})","g")
                    result = result.replace(reg,obj[key])
                } 
            }
        }else{
            for (var i = 0; i < obj.length; i++) {
                if (obj[i] != undefined) {
　　　　　　　　　　var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, obj[i]);
                }
            }
        }
    }
}
var _getMultilines = function(fun){
    // 利用函数内部多行注释功能 实现多行字符串功能
    lines = new String(fun);
    return lines.toString().replace(/^[^\/]+\/\*!?\s?/, '').replace(/\*\/[^\/]+$/, '');
}
var str = _getMultiliness(
    function(){
        /*!
        	<button type="button" id="{uuid}">
    			上传
			</button>
        */
    }
)
_format(str,{uuid:"dc3ccdc33b33kkjdj8900"})
```

## 4. file input value置空

```js
//IE不支持
jQuery('#fileinput').val('')
```

在IE下兼容，需要重置file input

```js
var u = navigator.userAgent;
if(u.indexOf('Trident') > -1){
    //clone file input
    var newFile = jQuery('#fileinput')[0].cloneNode(false);
   //注册原先的监听事件
    newFile.onchange = jQuery('#fileinput')[0].onchange;
    //替换新的file input
    jQuery('#fileinput')[0].parentNode.replaceChild(newFile,jQuery('#fileinput')[0]);
}else{
    jQuery('#fileinput').val('');
}
```

## 5. 获取浏览器信息

```js
var ua = navigator.userAgent;
ua.indexOf('Trident') > -1		======>	IE
ua.indexOf('Presto') > -1		======>	Opera
ua.indexOf('AppleWebKit') > -1	======> 苹果、谷歌
ua.indexOf('Gecko') > -1		======>	火狐
......
```

## 6. 浮点数精度问题

由于计算机存储二进制浮点数的表示导致的，其他语言有decimal库来规避，而JavaScript没有。一般处理办法，将浮点数转化为整数计算后再转化为浮点数。

```js
0.1+0.2  			======>   0.30000000000000004
(0.1*10+0.2*10)/10	======>   0.3
```

## 7. jQuery.Deferred

jQuery.Deferred的简单使用。

正常情况下，期待js控制的界面是异步的而且数据都能获取的。

<hr>

错误示范：

```js
var func1 = function () {
        var data = ''
        jQuery.ajax({
            url:'upload',
            type:'get',
            success:function (data) {
                console.log('第一步：请求消息')
                var data = JSON.parse(data)
            }
        });
        setTimeout(function () {
            console.log('第二步：',data)
        },100)
        console.log('第三步：继续流转');
        console.log('第四步：结束')
    }
```

输出结果：

```
第三步：继续流转
第四步：结束
第一步：请求消息
第二步
```

由于ajax请求和setTimeout都是耗时操作，所以这个示范的输出不是期望的。

使用回调复杂麻烦。。。

<hr>

使用jQuery.Deferred:

```js
function func2() {
        var req = jQuery.ajax({
            url:'upload',
            type:'get',
            success:function (data) {
                console.log('第一步：请求消息')
            }
        });
        req.then(function (data) {
            var data = JSON.parse(data);
            console.log('第二步：',data)
            var def = jQuery.Deferred()
            function f() {
                def.resolve('第三步：继续流转')
            }
            setTimeout(f,100)
            return def
        }).then(function (data) {
            console.log(data);
            console.log('第四步：结束')
        })
    }
```

输出结果：

```
第一步：请求消息
第二步： {msg: "OK"}
第三步：继续流转
第四步：结束
```

逻辑清晰，达到期望。

## 8. 事件冒泡

## 9. 数组操作

| 操作   | 描述 |
| ------ | ---- |
| push() |      |
| pop()  |      |
|        |      |





