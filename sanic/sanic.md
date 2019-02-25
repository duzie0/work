

# Sanic

## 描述

Sanic是类flask的异步框架。

Sanic使用Python3.5以上版本，以支持`async/await`语法。

使用异步框架则要异步到底，基本上任何`I/O`、耗时操作都要使用异步。

否则，适得其反，有些情况会降低系统性能。

## 开始

**安装：** `python3 -m pip install sanic`

**新建：** 新建`main.py`文件

```python
from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello":"world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9000)
```

**启动：** 执行命令`python3 main.py`

**访问：** 浏览器访问`http://127.0.0.1:9000`

## Sanic 类

`app = Sanic()`

#### url_for:

`app.url_for('index')`此处传字符串类型，传函数名报错。

#### static:

```python
app.static('/static', './static')
app.static('/uploads', './uploads', name='uploads')
```

第一个参数指的是URL中的路径显示，第二个参数指的是文件目录路径。name参数指的是该静态资源的名称。

```python
print(
    app.url_for('static', filename='aa.txt'), 
    app.url_for('static', name='uploads', filename='aa.jpg')
)
```

输出的结果为：

>/static/aa.txt 	
>
>/uploads/aa.jpg

### sanic 装饰器

#### `@app.route ` 路由

#### `@app.websocket`  websocket路由

一个 Websocket 路由的处理程序传递**请求**作为第一个参数，并且一个 **Websocket 协议对象**作为第二个 参数。该协议对象有 `send` 和 `recv` 方法来分别发送和接收数据。

**官方示例：**

```python
from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

app = Sanic()

@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)
```

#### `@app.exception` 异常

要复写 Sanic 的默认异常的处理

该装饰器需要一个异常列表作为参数来处理。你可以传递 `SanicException` 以捕获所有异常！被装饰的异常处理程序必须带一个 `Request` 和 `Exception` 对象作为参数。

**示例：**

```python
@app.exception(NotFound)
async def not_found_404(request, exception):
    return text('页面不存在，请联系管理员！')
```

#### `@app.middleware` 中间件

- `request`请求中间件
- `response`响应中间件

请求中间件仅接受`request`作为参数

响应中间件可以同时接收`request`和`response`作为参数

如果中间件**返回一个 `HTTPResponse` 对象**，该请求会停止处理并且响应会被返回。

**示例：**

```python
@app.middleware('request')
async def halt_request(request):
    return text("请求到这里结束，直接中断了。")
```

```python
@app.middleware('response')
async def halt_response(request,response):
    return text('响应到这里中断了。')
```

#### `@app.listener` 监听器

**四个监听器：**

- `before_server_start`
- `after_server_start`
- `before_server_stop`
- `after_server_stop`

这些监听器会在app对象以及asynccio loop的程序上作为装饰器来执行。

##  `HTTPResponse` 对象

使用 `sanic.response` 模块的函数创建响应。

| 名称                 | 描述                         |
| -------------------- | ---------------------------- |
| response.json        | JSON格式数据                 |
| response.text        | 富文本数据                   |
| response.html        | HTML数据                     |
| response.file        | 文件（涉及I/O要使用await）   |
| response.stream      | 流（涉及I/O要使用await）     |
| response.file_stream | 文件流（涉及I/O要使用await） |
| response.redirect    | 重定向                       |
| response.raw         | 不对body编码的响应           |

**修改请求头和状态码示例：**

```python
@app.route('/json')
async def modify_response(request):
    return sanic.response.json(
    	{"message": "Hello World!"},
        headers={"X-Served-By": "sanic"},
        status=200
    )
```

## 蓝图

用于拆分项目，将项目根据不同的业务逻辑拆分为不同的块。

构建项目的层次结构。

可插拔。

用于API版本。

**从示例来看蓝图：**

官方文档提供的结构：

```shell
api/
├──content/
│  ├──authors.py
│  ├──static.py
│  └──__init__.py
├──info.py
└──__init__.py
app.py
```

**`api/content/authors.py`**

```python
from sanic import BluePrint
from sanic.response import json

authors = BluePrint('authors', url_prefix='/authors')

#最终组织出的路径为 /api/content/authors/lisi
@authors.route('/lisi')
async def bp_authors(request): #注：方法名和蓝图对象不能重名，否则报错
    return json({"message":"Hello,I'm lisi."})
```

**`api/content/static.py`**

```python
from sanic import BluePrint
from sanic.response import json

static = BluePrint('static', url_prefix="/static")

#最终组织出的路径为 /api/content/static/png
@static.route('/png')
async def bp_static(request):
    return json({"message":"Hello,this is a picture."})
```

**`api/info.py`**

```python
from sanic import BluePrint
from sanic.response import json

#最终组织出的路径为 /api/info/msg
info = BluePrint('info', url_prefix='/info')

@info.route('/msg')
async def bp_info(request):
    return json({"message":"Hello,this is a message."})
```

**`api/content/__init__.py`**

```python
from sanic import BluePrint
from .authors import authors
from .static import static

content = BluePrint.group(authors, static, url_prefix='/content')
```

**`api/__init__.py`**

```python
from sanic import BluePrint
from .content import content
from .info import info

api = BluePrint.group(content, info, url_prefix='/api')
```

**`app.py`**

```python
from sanic import BluePrint, Sanic
from api import api

app = Sanic(__name__)
app.blueprint(api)
```

## 配置

**`config = app.config`**

config是一个对象。

```python
config.DB_NAME = 'app'
config.DB_USER = 'root'
```

或者

```python
db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'app',
    'DB_USER': 'root'
}
config.update(db_settings)
```

### 加载配置

#### 从环境变量中

任何被 `SANIC_` 前缀定义的变量将会被 sanic 配置接受。例如，设置 `SANIC_REQUEST_TIMEOUT` 将被应用程序自动加载并提供给 `REQUEST_TIMEOUT` 配置变量。你可以传递一个不同的前缀给 Sanic:

```
app = Sanic(load_env='MYAPP_')
```

以上的变量会是 `MYAPP_REQUEST_TIMEOUT`。如果你想要禁用从环境变量加载你可以用 `False` 替代它的设置:

```
app = Sanic(load_env=False)
```

#### 从一个对象中

如果有很多配置值并且它们有合理的默认值，将它们放入模块可能会有所帮助：

```
import myapp.default_settings

app = Sanic('myapp')
app.config.from_object(myapp.default_settings)
```

你也可以用一个类或者其他任何对象。

#### 从一个文件

通常你想要从一个不是分布式应用程序部分的文件加载配置。你可以使用 `from_pyfile(/path/to/config_file)` 来加载。但是，这需要程序知道配置文件的路径。相反，你可以在环境变量中指定配置文件的位置，并告诉 Sanic 使用它来查找配置文件。

```
app = Sanic('myapp')
app.config.from_envvar('MYAPP_SETTINGS')
```

然后，你可以使用 `MYAPP_SETTINGS` 环境变量集运行您的应用程序：

```
$ MYAPP_SETTINGS=/path/to/config_file python3 myapp.py
INFO: Goin' Fast @ http://0.0.0.0:8000
```

配置文件是为了加载它们而执行的普通 Python 文件。这允许你使用任意逻辑来建立正确的配置。只有大写的变量才能加入配置。最常见的配置由简单的键值对组成：

```
# config_file
DB_HOST = 'localhost'
DB_NAME = 'appdb'
DB_USER = 'appuser'
```

#### 内建配置值

```shell
| Variable           | Default   | Description                  	
| ------------------ | --------- | ---------------------------- 	
| REQUEST_MAX_SIZE   | 100000000 | 请求最大值 (bytes)     
| REQUEST_TIMEOUT    | 60        | 请求到达时间 (sec)				
| RESPONSE_TIMEOUT   | 60        | 响应处理时间 (sec) 			
| KEEP_ALIVE         | True      | 当 False 时禁用 keep-alive     
| KEEP_ALIVE_TIMEOUT | 5         | 一个 TCP 连接保持的时长 (sec)    
```

