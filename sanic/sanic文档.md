# 开始

在开始前请确保你同时安装了 [pip](https://pip.pypa.io/en/stable/installing/) 和至少 3.5 以上版本的 Python 。Sanic 使用了新的 `async`/`await`语法，所以之前的版本无法工作。

1. 安装 Sanic: `python3 -m pip install sanic`
2. 新建一个叫 `main.py` 的文件并且附上以下代码：

```
from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

1. 启动服务器: `python3 main.py`
2. 在你的浏览器打开地址 `http://0.0.0.0:8000`。你会看到 *Hello world!*。

现在你已经会用 Sanic 了！

# Routing

路由允许用户为不同的 URL 端指定处理函数。

一个基本的路由看起来如下，其中 `app` 是一个 `Sanic` 类的实例：

```
from sanic.response import json

@app.route("/")
async def test(request):
    return json({ "hello": "world" })
```

当 `http://server.url/` 这个 url 被访问 (服务器的根 url), 最后的 `/` 被路由匹配到 `test` 这个返回一个 JSON 对象的处理函数。

Sanic 处理函数必须使用 `async def` 语法来定义，因为他们是异步函数。



## 请求参数

Sanic 附带一个支持请求参数的基本路由。

要指定一个请求参数，用尖括号包裹如下： `<PARAM>`。请求参数作为关键字被传递到处理函数。

```
from sanic.response import text

@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))
```

要指定一个参数的类型，需在括号里定义的参数名后面加一个 `:type` 。如果参数匹配不到这个指定的类型， Sanic 将会抛出一个 `NotFound` 异常，在 URL 上以一个 `404: Page not found` 错误作为结果。

```
from sanic.response import text

@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))

@app.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))

@app.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))

@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))
```



## HTTP 请求方法

默认情况下，在一个 URL 上定义一个路由将只会对 GET 请求有效。然而， `@app.route` 装饰器接受一个可选的参数， `methods`，该参数允许处理函数处理 HTTP 请求方法列表中的任意一个方法。

```
from sanic.response import text

@app.route('/post', methods=['POST'])
async def post_handler(request):
    return text('POST request - {}'.format(request.json))

@app.route('/get', methods=['GET'])
async def get_handler(request):
    return text('GET request - {}'.format(request.args))
```

还有一个可选的 `host` 参数 (可以是一个 list 或 string)。这限定了一个路由到提供的主机或主机组。如果一个路由没有 host，这会设置默认。

```
@app.route('/get', methods=['GET'], host='example.com')
async def get_handler(request):
    return text('GET request - {}'.format(request.args))

# if the host header doesn't match example.com, this route will be used
@app.route('/get', methods=['GET'])
async def get_handler(request):
    return text('GET request in default - {}'.format(request.args))
```

还有简写方法装饰器：

```
from sanic.response import text

@app.post('/post')
async def post_handler(request):
    return text('POST request - {}'.format(request.json))

@app.get('/get')
async def get_handler(request):
    return text('GET request - {}'.format(request.args))
```



## `add_route` 方法

正如我们看到的，路由经常由 `@app.route` 装饰器来指定。然而，这个装饰器其实只是一个 `app.add_route` 方法的包装，用法如下：

```
from sanic.response import text

# Define the handler functions
async def handler1(request):
    return text('OK')

async def handler2(request, name):
    return text('Folder - {}'.format(name))

async def person_handler2(request, name):
    return text('Person - {}'.format(name))

# Add each handler function as a route
app.add_route(handler1, '/test')
app.add_route(handler2, '/folder/<name>')
app.add_route(person_handler2, '/person/<name:[A-z]>', methods=['GET'])
```



## URL 由 `url_for` 创建

Sanic 提供了一个 `url_for` 方法来生成一组基于这个处理方法名称的 URL。如果你想在 app 中避免硬编码 url，这是有用的。相反，你可以只参考这个处理名称。举个例子：

```
from sanic.response import redirect

@app.route('/')
async def index(request):
    # generate a URL for the endpoint `post_handler`
    url = app.url_for('post_handler', post_id=5)
    # the URL is `/posts/5`, redirect to it
    return redirect(url)    

@app.route('/posts/<post_id>')
async def post_handler(request, post_id):
    return text('Post - {}'.format(post_id))
```

在使用 `url_for` 时需要注意的其他事项：

- 关键字参数传递给 `url_for` 不是请求参数将会被包括在 URL 的请求参数里。例如：

```
url = app.url_for('post_handler', post_id=5, arg_one='one', arg_two='two')
# /posts/5?arg_one=one&arg_two=two
```

- 多元的参数也会被 `url_for` 传递。例如：

```
url = app.url_for('post_handler', post_id=5, arg_one=['one', 'two'])
# /posts/5?arg_one=one&arg_one=two
```

- 还有一些特殊的参数 (`_anchor`, `_external`, `_scheme`, `_method`, `_server`) 传递到 `url_for` 会有一个指定的 url 建立 (`_method` 现在不被支持并且会被忽略)。例如：

```
url = app.url_for('post_handler', post_id=5, arg_one='one', _anchor='anchor')
# /posts/5?arg_one=one#anchor

url = app.url_for('post_handler', post_id=5, arg_one='one', _external=True)
# //server/posts/5?arg_one=one
# _external requires passed argument _server or SERVER_NAME in app.config or url will be same as no _external

url = app.url_for('post_handler', post_id=5, arg_one='one', _scheme='http', _external=True)
# http://server/posts/5?arg_one=one
# when specifying _scheme, _external must be True

# you can pass all special arguments one time
url = app.url_for('post_handler', post_id=5, arg_one=['one', 'two'], arg_two=2, _anchor='anchor', _scheme='http', _external=True, _server='another_server:8888')
# http://another_server:8888/posts/5?arg_one=one&arg_one=two&arg_two=2#anchor
```

- 所有有效的参数必须被传递到 `url_for` 用来建立一个 URL。如果一个参数没有提供，或者没有匹配到指定的类型，会抛出一个 `URLBuildError`。



## WebSocket 路由

对于 WebSocket 协议的路由可以使用 `@app.websocket` 装饰器定义：

```
@app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = 'hello!'
        print('Sending: ' + data)
        await ws.send(data)
        data = await ws.recv()
        print('Received: ' + data)
```

另外, `app.add_websocket_route` 方法可以用来替代这个装饰器：

```
async def feed(request, ws):
    pass

app.add_websocket_route(my_websocket_handler, '/feed')
```

一个 WebSocket 路由的处理程序作为第一个参数传递请求，同时一个 WebSocket 协议对象作为第二个参数。这个协议对象有 `send` 和 `recv` 方法分别发送和接受数据。

支持 WebSocket 需要 Aymeric Augustin 提供的 [websockets](https://github.com/aaugustin/websockets) 包。



## 关于 `strict_slashes`

你可以设计严格的 `routes` 来决定要不要斜线。它是可配置的。

```
# provide default strict_slashes value for all routes
app = Sanic('test_route_strict_slash', strict_slashes=True)

# you can also overwrite strict_slashes value for specific route
@app.get('/get', strict_slashes=False)
def handler(request):
    return text('OK')

# It also works for blueprints
bp = Blueprint('test_bp_strict_slash', strict_slashes=True)

@bp.get('/bp/get', strict_slashes=False)
def handler(request):
    return text('OK')

app.blueprint(bp)
```



## 用户定义路由命名

你可以传递 `name` 来改变路由命名以避免使用默认命名 (`handler.__name__`)。

```
app = Sanic('test_named_route')

@app.get('/get', name='get_handler')
def handler(request):
    return text('OK')

# then you need use `app.url_for('get_handler')`
# instead of # `app.url_for('handler')`

# It also works for blueprints
bp = Blueprint('test_named_bp')

@bp.get('/bp/get', name='get_handler')
def handler(request):
    return text('OK')

app.blueprint(bp)

# then you need use `app.url_for('test_named_bp.get_handler')`
# instead of `app.url_for('test_named_bp.handler')`

# different names can be used for same url with different methods

@app.get('/test', name='route_test')
def handler(request):
    return text('OK')

@app.post('/test', name='route_post')
def handler2(request):
    return text('OK POST')

@app.put('/test', name='route_put')
def handler3(request):
    return text('OK PUT')

# below url are the same, you can use any of them
# '/test'
app.url_for('route_test')
# app.url_for('route_post')
# app.url_for('route_put')

# for same handler name with different methods
# you need specify the name (it's url_for issue)
@app.get('/get')
def handler(request):
    return text('OK')

@app.post('/post', name='post_handler')
def handler(request):
    return text('OK')

# then
# app.url_for('handler') == '/get'
# app.url_for('post_handler') == '/post'
```



## 为静态资源建立 URL

现在你可以使用 `url_for` 给静态资源建立 url。如果是为文件直传的， `filename` 会被忽略。

```
app = Sanic('test_static')
app.static('/static', './static')
app.static('/uploads', './uploads', name='uploads')
app.static('/the_best.png', '/home/ubuntu/test.png', name='best_png')

bp = Blueprint('bp', url_prefix='bp')
bp.static('/static', './static')
bp.static('/uploads', './uploads', name='uploads')
bp.static('/the_best.png', '/home/ubuntu/test.png', name='best_png')
app.blueprint(bp)

# then build the url
app.url_for('static', filename='file.txt') == '/static/file.txt'
app.url_for('static', name='static', filename='file.txt') == '/static/file.txt'
app.url_for('static', name='uploads', filename='file.txt') == '/uploads/file.txt'
app.url_for('static', name='best_png') == '/the_best.png'

# blueprint url building
app.url_for('static', name='bp.static', filename='file.txt') == '/bp/static/file.txt'
app.url_for('static', name='bp.uploads', filename='file.txt') == '/bp/uploads/file.txt'
app.url_for('static', name='bp.best_png') == '/bp/static/the_best.png'
```

# 请求数据

当一端接收一个 HTTP 请求，路由函数会传递一个 `Request` 对象。

下面的变量作为 `Request` 对象的属性是可访问的：

- `json` (任意类型) - JSON body

  ```
  from sanic.response import json
  
  @app.route("/json")
  def post_json(request):
      return json({ "received": True, "message": request.json })
  ```

- `args` (字典) - 请求参数的变量。 一个请求参数就是一个类似 `?key1=value1&key2=value2` URL 的一部分。如果都被解析了，那么 `args` 字典数据就是 `{'key1': ['value1'], 'key2': ['value2']}`。 这个请求的 `query_string` 变量保存了未被解析的字符数据。

  ```
  from sanic.response import json
  
  @app.route("/query_string")
  def query_string(request):
      return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })
  ```

- `raw_args` (字典) - 很多情况你需要访问一个较少包装的字典的 url 参数。对于同样上一个 URL `?key1=value1&key2=value2`， `raw_args` 字典会是 `{'key1': 'value1', 'key2': 'value2'}`。

- `files` (`File` 对象的字典) - 文件列表，包括 name, body, 和 type

  ```
  from sanic.response import json
  
  @app.route("/files")
  def post_json(request):
      test_file = request.files.get('test')
  
      file_parameters = {
          'body': test_file.body,
          'name': test_file.name,
          'type': test_file.type,
      }
  
      return json({ "received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters })
  ```

- `form` (字典) - 提交 form 变量。

  ```
  from sanic.response import json
  
  @app.route("/form")
  def post_json(request):
      return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })
  ```

- `body` (bytes) - 提交原始请求体数据。这个属性允许请求的原始数据的获取而不管内容的类型。

  ```
  from sanic.response import text
  
  @app.route("/users", methods=["POST",])
  def create_user(request):
      return text("You are trying to create a user with the following POST: %s" % request.body)
  ```

- `headers` (字典) - 一个例子-不严格区分的包含请求头部的字典。

- `method` (字符) - HTTP 请求方法 (ie `GET`, `POST`)。

- `ip` (字符) - 请求 IP 地址。

- `port` (字符) - 请求的地址端口。

- `socket` (元组) - 请求的 (IP, port).

- `app` - 一个处理请求的 Sanic 程序对象的引用。当一些包含蓝图或其他处理函数的模块中没有访问 `app` 对象的权限时有用。

  ```
  from sanic.response import json
  from sanic import Blueprint
  
  bp = Blueprint('my_blueprint')
  
  @bp.route('/')
  async def bp_root(request):
      if request.app.config['DEBUG']:
          return json({'status': 'debug'})
      else:
          return json({'status': 'production'})
  ```

- `url`: 请求的完整 URL， ie: `http://localhost:8000/posts/1/?foo=bar`

- `scheme`: 与请求相关联的 URL 方案: `http` 或 `https`

- `host`: 与请求相关联的主机: `localhost:8080`

- `path`: 请求的路径: `/posts/1/`

- `query_string`: 请求的参数: `foo=bar` 或者空的字符 `''`

- `uri_template`: 匹配路由程序的模板： `/posts/<id>/`

- `token`: 认证头部的值: `Basic YWRtaW46YWRtaW4=`



## 用 `get` 和 `getlist` 访问值

返回字典的请求数据实际返回了一个叫做 `RequestParameters` 的 `dict` 的子类。使用这个对象的关键区别在于 `get` 和 `getlist` 方法之间的区别。

- `get(key, default=None)` 正常执行，除非给定的 key 的值 是一个列表，*只返回第一个元素*。
- `getlist(key, default=None)` 正常执行，*返回整个列表*.

```
from sanic.request import RequestParameters

args = RequestParameters()
args['titles'] = ['Post 1', 'Post 2']

args.get('titles') # => 'Post 1'

args.getlist('titles') # => ['Post 1', 'Post 2']
```

# 响应

使用 `sanic.response` 模块的函数创建响应。



## 富文本

```
from sanic import response


@app.route('/text')
def handle_request(request):
    return response.text('Hello world!')
```



## HTML

```
from sanic import response


@app.route('/html')
def handle_request(request):
    return response.html('<p>Hello world!</p>')
```



## JSON

```
from sanic import response


@app.route('/json')
def handle_request(request):
    return response.json({'message': 'Hello world!'})
```



## 文件

```
from sanic import response


@app.route('/file')
async def handle_request(request):
    return await response.file('/srv/www/whatever.png')
```



## 流

```
from sanic import response

@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        response.write('foo')
        response.write('bar')
    return response.stream(streaming_fn, content_type='text/plain')
```



## 文件流

对于大文件，会结合以上的 文件 和 流 实现。

```
from sanic import response

@app.route('/big_file.png')
async def handle_request(request):
    return await response.file_stream('/srv/www/whatever.png')
```



## 重定向

```
from sanic import response


@app.route('/redirect')
def handle_request(request):
    return response.redirect('/json')
```



## Raw

不对 body 编码的响应

```
from sanic import response


@app.route('/raw')
def handle_request(request):
    return response.raw(b'raw data')
```



## 修改 头部 或 状态码

要修改头部或状态码，传递 `headers` 或 `status` 参数给这些函数：

```
from sanic import response


@app.route('/json')
def handle_request(request):
    return response.json(
        {'message': 'Hello world!'},
        headers={'X-Served-By': 'sanic'},
        status=200
    )
```

# 静态资源

静态文件和目录，如图像文件，会在注册 `app.static` 方法后提供服务。该方法采用端 URL 和文件名。指定的文件将通过给定的端被访问。

```
from sanic import Sanic
from sanic.blueprints import Blueprint

app = Sanic(__name__)

# Serves files from the static folder to the URL /static
app.static('/static', './static')
# use url_for to build the url, name defaults to 'static' and can be ignored
app.url_for('static', filename='file.txt') == '/static/file.txt'
app.url_for('static', name='static', filename='file.txt') == '/static/file.txt'

# Serves the file /home/ubuntu/test.png when the URL /the_best.png
# is requested
app.static('/the_best.png', '/home/ubuntu/test.png', name='best_png')

# you can use url_for to build the static file url
# you can ignore name and filename parameters if you don't define it
app.url_for('static', name='best_png') == '/the_best.png'
app.url_for('static', name='best_png', filename='any') == '/the_best.png'

# you need define the name for other static files
app.static('/another.png', '/home/ubuntu/another.png', name='another')
app.url_for('static', name='another') == '/another.png'
app.url_for('static', name='another', filename='any') == '/another.png'

# also, you can use static for blueprint
bp = Blueprint('bp', url_prefix='/bp')
bp.static('/static', './static')

# servers the file directly
bp.static('/the_best.png', '/home/ubuntu/test.png', name='best_png')
app.blueprint(bp)

app.url_for('static', name='bp.static', filename='file.txt') == '/bp/static/file.txt'
app.url_for('static', name='bp.best_png') == '/bp/test_best.png'

app.run(host="0.0.0.0", port=8000)
```

# 异常

异常可以在请求处理程序中抛出并且自动地被 Sanic 处理。异常用一个消息作为第一个参数，同时也能携带一个状态码在 HTTP 响应中回传。



## 抛出一个异常

要抛出一个异常，只需从 `sanic.exceptions` 模块 `raise` 抛出相关的异常。

```
from sanic.exceptions import ServerError

@app.route('/killme')
async def i_am_ready_to_die(request):
    raise ServerError("Something bad happened", status_code=500)
```

你也可以使用 `abort` 函数附上合适状态码：

```
from sanic.exceptions import abort
from sanic.response import text

@app.route('/youshallnotpass')
async def no_no(request):
        abort(401)
        # this won't happen
        text("OK")
```



## 处理异常

要复写 Sanic 的默认异常的处理，就要用到 `@app.exception` 装饰器。该装饰器需要一个异常列表作为参数来处理。你可以传递 `SanicException` 以捕获所有异常！被装饰的异常处理程序必须带一个 `Request` 和 `Exception` 对象作为参数。

```
from sanic.response import text
from sanic.exceptions import NotFound

@app.exception(NotFound)
async def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))
```



## 有用的异常

几个最有用的异常如下所示：

- `NotFound`: 当对请求对应的路由没有找到时被调用。
- `ServerError`: 当服务器发生了某些错误是被调用。这通常在用户代码里引发异常时发生。

参考 `sanic.exceptions` 模块以获取抛出异常的完整的列表。

# 中间件 和 监听器

中间件是在请求到服务器前或后执行的程序。它们能用来修改请求到用户定义的处理程序或者从用户定义的处理程序中响应。

另外，Sanic 提供的监听器允许你在应用程序生命周期的多个端运行代码



## 中间件

有两种中间件：请求和响应。两者都使用 `@app.middleware` 装饰器声明，装饰器的参数是一个表示类型的字符串：`'request'` 或 `'response'`.

- 请求中间件接收仅作为 `request` 的参数。
- 响应中间件接收同时可以是 `request` 和 `response` 的参数。

最简单的中间件根本不会修改请求和响应：

```
@app.middleware('request')
async def print_on_request(request):
    print("I print when a request is received by the server")

@app.middleware('response')
async def print_on_response(request, response):
    print("I print when a response is returned by the server")
```



## 修改请求或响应

中间件可以修改给定的请求或响应的参数，*只要它们不返回*。下面的例子显示了这个实际的用例：

```
app = Sanic(__name__)

@app.middleware('response')
async def custom_banner(request, response):
    response.headers["Server"] = "Fake-Server"

@app.middleware('response')
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"

app.run(host="0.0.0.0", port=8000)
```

以上代码会按顺序接收两个中间件。第一个中间件 **custom_banner** 会修改 HTTP 响应头 *Server* 为 *Fake-Server*，第二个中间件 **prevent_xss** 会添加 HTTP 头以避免跨站脚本 (XSS) 攻击。这两个程序在用户程序返回响应后调用。



## 提前响应

如果中间件返回一个 `HTTPResponse` 对象，该请求会停止处理并且响应会被返回。如果这发生在一个到达相应用户路由处理程序前的请求，该处理程序永远不会被调用。返回响应也会阻止任何进一步的中间件运行。

```
@app.middleware('request')
async def halt_request(request):
    return text('I halted the request')

@app.middleware('response')
async def halt_response(request, response):
    return text('I halted the response')
```



## 监听器

如果你想执行 startup/teardown 代码作为你服务应用的启动或关闭，你可以使用以下监听器：

- `before_server_start`
- `after_server_start`
- `before_server_stop`
- `after_server_stop`

这些监听器会在 app 对象以及 asyncio loop 的程序上作为装饰器来执行。

例如：

```
@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = await db_setup()

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print('Server successfully started!')

@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')

@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.db.close()
```

也有可能使用 `register_listener` 方法来注册监听器。如果你定义你的监听器在一个当你已经实例化你的 app 后的别的模块上，这方法就会有用。

```
app = Sanic()

async def setup_db(app, loop):
    app.db = await db_setup()

app.register_listener(setup_db, 'before_server_start')
```

如果你想要在 loop 已经启动后安排一个后台任务来执行，Sanic 提供了 `add_task` 方法来简单地实现。

```
async def notify_server_started_after_five_seconds():
    await asyncio.sleep(5)
    print('Server successfully started!')

app.add_task(notify_server_started_after_five_seconds())
```

Sanic 会尝试自动注入 app，作为参数传递给任务：

```
async def notify_server_started_after_five_seconds(app):
    await asyncio.sleep(5)
    print(app.name)

app.add_task(notify_server_started_after_five_seconds)
```

或者同样效果地你可以明确地传递 app

```
async def notify_server_started_after_five_seconds(app):
    await asyncio.sleep(5)
    print(app.name)

app.add_task(notify_server_started_after_five_seconds(app))
```

# 蓝图

蓝图 (Blueprints) 是用在一个应用程序里可用作子路由的对象。作为添加路由到应用程序实例的替代者，蓝图为添加路由定义了相似的方法，即用一种灵活而且可插拔的方法注册到应用程序实例。

蓝图对于大型应用特别有用，当你的应用逻辑能被分解成若干个组或者责任区域。



## 我的第一个蓝图

以下展示了一个非常简单的蓝图，即在你的应用的根 url `/` 注册了一个处理程序。

假设你保存了这个一会儿能被 import 到你的主应用的文件 `my_blueprint.py`。

```
from sanic.response import json
from sanic import Blueprint

bp = Blueprint('my_blueprint')

@bp.route('/')
async def bp_root(request):
    return json({'my': 'blueprint'})
```



## 注册蓝图

蓝图必须被应用程序注册。

```
from sanic import Sanic
from my_blueprint import bp

app = Sanic(__name__)
app.blueprint(bp)

app.run(host='0.0.0.0', port=8000, debug=True)
```

这将会添加蓝图到应用程序并且注册任意的被蓝图定义的路由。在 `app.router` 里已经注册的路由看起来如下：

```
[Route(handler=<function bp_root at 0x7f908382f9d8>, methods=None, pattern=re.compile('^/$'), parameters=[])]
```



## 蓝图 组 和 嵌套

蓝图也可能作为一个列表或元组的部分进行注册，其中注册员将递归地遍历蓝图的任何子序列并相应地注册它们。`Blueprint.group` 方法提供简化的程序，允许一个 '模拟' 后端目录结构模仿从前端看到的东西。考虑这个 (颇有认为的) 例子：

```
api/
├──content/
│  ├──authors.py
│  ├──static.py
│  └──__init__.py
├──info.py
└──__init__.py
app.py
```

应用的蓝图的初始化层次结构如下所示：

```
# api/content/authors.py
from sanic import Blueprint

authors = Blueprint('content_authors', url_prefix='/authors')
# api/content/static.py
from sanic import Blueprint

static = Blueprint('content_static', url_prefix='/static')
# api/content/__init__.py
from sanic import Blueprint

from .static import static
from .authors import authors

content = Blueprint.group(assets, authors, url_prefix='/content')
# api/info.py
from sanic import Blueprint

info = Blueprint('info', url_prefix='/info')
# api/__init__.py
from sanic import Blueprint

from .content import content
from .info import info

api = Blueprint.group(content, info, url_prefix='/api')
```

在 `app.py` 中注册这些蓝图现在可以这样完成：

```
# app.py
from sanic import Sanic

from .api import api

app = Sanic(__name__)

app.blueprint(api)
```



## 使用蓝图

蓝图具有与应用程序实例相同的功能。



### WebSocket 路由

WebSocket 处理程序能够使用 `@bp.websocket` 装饰器或者 `bp.add_websocket_route` 方法在蓝图注册。



### 中间件

使用蓝图允许你可以全局地注册中间件。

```
@bp.middleware
async def print_on_request(request):
    print("I am a spy")

@bp.middleware('request')
async def halt_request(request):
    return text('I halted the request')

@bp.middleware('response')
async def halt_response(request, response):
    return text('I halted the response')
```



### 异常

异常可以被专门用于全局的蓝图。

```
@bp.exception(NotFound)
def ignore_404s(request, exception):
    return text("Yep, I totally found the page: {}".format(request.url))
```



### 静态文件

静态文件可以在蓝图前缀下全局提供。

```
# suppose bp.name == 'bp'

bp.static('/web/path', '/folder/to/serve')
# also you can pass name parameter to it for url_for
bp.static('/web/path', '/folder/to/server', name='uploads')
app.url_for('static', name='bp.uploads', filename='file.txt') == '/bp/web/path/file.txt'
```



## 启动和停止

蓝图可以在服务器启动和停止程序期间运行程序。如果在多进程模式 (多于一个 worker) 运行，他们会在 workers fork 之后被触发。

有效的事件如下:

- `before_server_start`: 在服务器开始接收连接之前执行
- `after_server_start`: 在服务器开始接收连接之后执行
- `before_server_stop`: 在服务器停止接收连接之前执行
- `after_server_stop`: 在服务器停止并且所有请求已经问你成之后执行

```
bp = Blueprint('my_blueprint')

@bp.listener('before_server_start')
async def setup_connection(app, loop):
    global database
    database = mysql.connect(host='127.0.0.1'...)

@bp.listener('after_server_stop')
async def close_connection(app, loop):
    await database.close()
```



## 用例: API 版本

蓝图能很好的用于 API 版本，一个蓝图可以指向 `/v1/<routes>`，另一个指向 `/v2/<routes>`。

当一个蓝图初始化了，它可以带一个可选的 `url_prefix` 参数，该参数将被添加到所有在蓝图定义的路由中。这个功能可以被用来执行我们的 API 版本方案。

```
# blueprints.py
from sanic.response import text
from sanic import Blueprint

blueprint_v1 = Blueprint('v1', url_prefix='/v1')
blueprint_v2 = Blueprint('v2', url_prefix='/v2')

@blueprint_v1.route('/')
async def api_v1_root(request):
    return text('Welcome to version 1 of our documentation')

@blueprint_v2.route('/')
async def api_v2_root(request):
    return text('Welcome to version 2 of our documentation')
```

当我们在 app 上注册了我们的蓝图，这些路由 `/v1` 和 `/v2` 现在将指向独立的蓝图，允许为每一个 API 版本创建 *子站点*

```
# main.py
from sanic import Sanic
from blueprints import blueprint_v1, blueprint_v2

app = Sanic(__name__)
app.blueprint(blueprint_v1, url_prefix='/v1')
app.blueprint(blueprint_v2, url_prefix='/v2')

app.run(host='0.0.0.0', port=8000, debug=True)
```



## 用 `url_for` 建立 URL

如果你希望为蓝图里的路由生成 URL，记住端点命名带着 `<blueprint_name>.<handler_name>` 格式。例如：

```
@blueprint_v1.route('/')
async def root(request):
    url = request.app.url_for('v1.post_handler', post_id=5) # --> '/v1/post/5'
    return redirect(url)


@blueprint_v1.route('/post/<post_id>')
async def post_handler(request, post_id):
    return text('Post {} in Blueprint V1'.format(post_id))
```

# WebSocket

Sanic 支持 websockets, 建立一个 WebSocket:

```
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

另外, `app.add_websocket_route` 方法能被用来替换装饰器:

```
async def feed(request, ws):
    pass

app.add_websocket_route(feed, '/feed')
```

一个 Websocket 路由的处理程序传递请求作为第一个参数，并且一个 Websocket 协议对象作为第二个 参数。该协议对象有 `send` 和 `recv` 方法来分别发送和接收数据。

你可以通过 `app.config` 建立你自己的 WebSocket 配置, 就像

想要了解更多请去 `Configuration` 章节。

# 配置

任何相当复杂的应用程序都需要配置，，这些配置不会被绑定到实际的代码中。对于不同环境和安装的设置可能也不同。



## 基础

Sanic 在应用程序对象的 `config` 属性中拥有配置。该配置对象仅是一个对象因此能被使用点号或者像一个字典一样修改:

```
app = Sanic('myapp')
app.config.DB_NAME = 'appdb'
app.config.DB_USER = 'appuser'
```

由于配置对象实际上是一个字典，你可以用它的 `update` 方法来一次性设置一些值:

```
db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)
```

一般来说，惯例只能有大写的配置参数。下面描述的用于加载配置的方法仅查找这样的大写参数。



## 加载配置

下面是一些如果加载配置的方法。



### 从环境变量

任何被 `SANIC_` 前缀定义的变量将会被 sanic 配置接受。例如，设置 `SANIC_REQUEST_TIMEOUT` 将被应用程序自动加载并提供给 `REQUEST_TIMEOUT` 配置变量。你可以传递一个不同的前缀给 Sanic:

```
app = Sanic(load_env='MYAPP_')
```

以上的变量会是 `MYAPP_REQUEST_TIMEOUT`。如果你想要禁用从环境变量加载你可以用 `False` 替代它的设置:

```
app = Sanic(load_env=False)
```



### 从一个对象

如果有很多配置值并且它们有合理的默认值，将它们放入模块可能会有所帮助：

```
import myapp.default_settings

app = Sanic('myapp')
app.config.from_object(myapp.default_settings)
```

你也可以用一个类或者其他任何对象。



### 从一个文件

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



## 内建的配置值

开箱即用只有几个预定的能在创建应用程序时被复写的值。

```
| Variable           | Default   | Description                                   |
| ------------------ | --------- | --------------------------------------------- |
| REQUEST_MAX_SIZE   | 100000000 | 请求最大值 (bytes)              |
| REQUEST_TIMEOUT    | 60        | 请求到达时间 (sec)   |
| RESPONSE_TIMEOUT   | 60        | 响应处理时间 (sec) |
| KEEP_ALIVE         | True      | 当 False 时禁用 keep-alive                |
| KEEP_ALIVE_TIMEOUT | 5         | 一个 TCP 连接保持的时长 (sec)  |
```



### 不同的超时变量:

一个请求超时衡量了在一个新的开放的 TCP 连接传递到 Sanic 后端服务的瞬间，和当整个 HTTP 请求已经接收的瞬间之间的时间差。如果这个时间超过了 `REQUEST_TIMEOUT` 值 (秒)，这被认为是客户端错误，因此 Sanic 生成一个 HTTP 408 响应并发送给客户端。调高这个值如果你的客户端经常传递非常大的请求负荷或者上传请求非常慢。

一个响应超时衡量了在一个 Sanic 服务器传递 HTTP 请求到 Sanic APP的瞬间，和一个 HTTP 响应发送到客户端的瞬间之间的时间差。如果这个时间超过了 `RESPONSE_TIMEOUT` 值 (秒)，这被认为是服务器的错误，因此 Sanic 生成一个 HTTP 503 响应并设置响应给客户端。调高这个值如果你的应用程序很可能有长时间运行的程序导致延迟了响应的产生。



### 什么是 Keep Alive？Keep Alive Timeout 是干嘛的？

Keep-Alive 是一个在 HTTP 1.1 里介绍的 HTTP 功能。当发送一个 HTTP 请求时，这个客户端 (通常是一个网络浏览器) 可以设置一个 Keep-Alive 头来指示 http 服务器 (Sanic) 不要在发送响应后关闭 TCP 连接。这允许客户端复用存在的 TCP 连接来发送随后的 HTTP 请求，确保为客户端和服务端提供更加高效的网络质量。

`KEEP_ALIVE` 配置变量默认被设置为 `True`。如果你的应用程序不需要这个功能，设置 `False` 使所有客户端连接在响应被发送后立即关闭，无论请求的 Keep-Alive 头如何。

服务器保持打开 TCP 连接的时间量由服务器自己决定。在 Sanic，这个值通过 `KEEP_ALIVE_TIMEOUT`值来配置。默认是 5 秒，与 Apache HTTP 服务器一样的配置，这在允许足够的时间为客户端发送一个新的请求和不用一次性保持太多连接之间提供了很好的平衡。不要超过 75 秒除非你知道你的客户端使用了支持 TCP 长连接。

参考：

```
Apache httpd server default keepalive timeout = 5 seconds
Nginx server default keepalive timeout = 75 seconds
Nginx performance tuning guidelines uses keepalive = 15 seconds
IE (5-9) client hard keepalive limit = 60 seconds
Firefox client hard keepalive limit = 115 seconds
Opera 11 client hard keepalive limit = 120 seconds
Chrome 13+ client keepalive limit > 300+ seconds
```

# Cookies

Cookies 是用户浏览器内部的一些数据。Sanic 可以读取和写入存储为键值对的 cookie 。

## 读 cookies

一个用户的 cookies 可以通过 `Request` 对象的 `cookies` 字典访问。

```
from sanic.response import text

@app.route("/cookie")
async def test(request):
    test_cookie = request.cookies.get('test')
    return text("Test cookie set to: {}".format(test_cookie))
```

## 写 cookies

当返回一个响应，cookies 可以在 `Response` 对象上设置。

```
from sanic.response import text

@app.route("/cookie")
async def test(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response
```

## 删除 cookies

Cookies 可以语义地或明确地删除。

```
from sanic.response import text

@app.route("/cookie")
async def test(request):
    response = text("Time to eat some cookies muahaha")

    # This cookie will be set to expire in 0 seconds
    del response.cookies['kill_me']

    # This cookie will self destruct in 5 seconds
    response.cookies['short_life'] = 'Glad to be here'
    response.cookies['short_life']['max-age'] = 5
    del response.cookies['favorite_color']

    # This cookie will remain unchanged
    response.cookies['favorite_color'] = 'blue'
    response.cookies['favorite_color'] = 'pink'
    del response.cookies['favorite_color']

    return response
```

响应 cookies 可被设置成字典值并且有一下有效参数:

- `expires` (datetime): cookies 在客户端的浏览器上的过期时间。
- `path` (string): cookie 使用的子 URL。默认为 /.
- `comment` (string): 注释 (元数据).
- `domain` (string): cookie 有效的指定域名。一个明确的指定域名必须总是有 . 开始。
- `max-age` (number): cookie 可以存活的最大秒数。
- `secure` (boolean): 指定 cookie 是否只能通过 HTTPS 发送。
- `httponly` (boolean): 指定 cookie 是否不能被 Javascript 读取。

# 处理装饰器

由于 Sanic 处理程序是简单的 Python 函数，你可以用类似 Flask 的方法用装饰器包裹他们。一个经典的用例就是当你想要在处理程序的代码执行前先运行一些代码。



## 认证装饰器

假设你想要检查一个用户是否被授权去访问特定端点。你可以创建一个装饰器来包裹一个处理程序，检查一个请求是否客户端被授权去访问一个资源，并且发送一个合理的响应。

```
from functools import wraps
from sanic.response import json

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


@app.route("/")
@authorized()
async def test(request):
    return json({status: 'authorized'})
```

# 流



## 请求流

Sanic 允许你通过流来获取请求，如下。当请求结束，`request.stream.get()` 返回 `None`。只有 post、 put 和 patch 装饰器才能有流参数。

```
from sanic import Sanic
from sanic.views import CompositionView
from sanic.views import HTTPMethodView
from sanic.views import stream as stream_decorator
from sanic.blueprints import Blueprint
from sanic.response import stream, text

bp = Blueprint('blueprint_request_stream')
app = Sanic('request_stream')


class SimpleView(HTTPMethodView):

    @stream_decorator
    async def post(self, request):
        result = ''
        while True:
            body = await request.stream.get()
            if body is None:
                break
            result += body.decode('utf-8')
        return text(result)


@app.post('/stream', stream=True)
async def handler(request):
    async def streaming(response):
        while True:
            body = await request.stream.get()
            if body is None:
                break
            body = body.decode('utf-8').replace('1', 'A')
            response.write(body)
    return stream(streaming)


@bp.put('/bp_stream', stream=True)
async def bp_handler(request):
    result = ''
    while True:
        body = await request.stream.get()
        if body is None:
            break
        result += body.decode('utf-8').replace('1', 'A')
    return text(result)


async def post_handler(request):
    result = ''
    while True:
        body = await request.stream.get()
        if body is None:
            break
        result += body.decode('utf-8')
    return text(result)

app.blueprint(bp)
app.add_route(SimpleView.as_view(), '/method_view')
view = CompositionView()
view.add(['POST'], post_handler, stream=True)
app.add_route(view, '/composition_view')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
```



## 响应流

Sanic 允许您使用流方法将内容传输到客户端。此方法接受通过写入的 `StreamingHTTPResponse` 对象传递的协程回调。一个简单的例子如下：

```
from sanic import Sanic
from sanic.response import stream

app = Sanic(__name__)

@app.route("/")
async def test(request):
    async def sample_streaming_fn(response):
        response.write('foo,')
        response.write('bar')

    return stream(sample_streaming_fn, content_type='text/csv')
```

这会在当你想要用流的方法将内容发送到来自外部服务的客户端的情况下变得有用，就像数据库。例如，你可以用流的方法将 `asyncpg` 提供的异步游标把数据记录发送到客户端：

```
@app.route("/")
async def index(request):
    async def stream_from_db(response):
        conn = await asyncpg.connect(database='test')
        async with conn.transaction():
            async for record in conn.cursor('SELECT generate_series(0, 10)'):
                response.write(record[0])

    return stream(stream_from_db)
```

# 基于类的视图

基于类的视图只是实现对请求的响应行为的类。它们提供了在同一个端点上划分不同HTTP请求类型的处理方式。相当与定义和装饰了三种不同的处理程序，每端支持一种请求类型，端点可以被分配一个基于类的视图。



## 定义视图

一个基于类的视图应该继承 `HTTPMethodView`。你可以为每个你想要支持的 HTTP 请求类型执行类方法。如果请求已经接收但是没有定义方法，一个 `405: Method not allowed` 响应就会生成。

要注册一个基于类的视图到端，`app.add_route` 方法是有用的。第一个参数应该是被定义带 `as_view`方法的类，第二个参数应该是 URL 端。

有效的方法有 `get`, `post`, `put`, `patch` 和 `delete`。一个使用所有方法的类看起来如下。

```
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic('some_name')

class SimpleView(HTTPMethodView):

  def get(self, request):
      return text('I am get method')

  def post(self, request):
      return text('I am post method')

  def put(self, request):
      return text('I am put method')

  def patch(self, request):
      return text('I am patch method')

  def delete(self, request):
      return text('I am delete method')

app.add_route(SimpleView.as_view(), '/')
```

你也可以使用 `async` 语法。

```
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

app = Sanic('some_name')

class SimpleAsyncView(HTTPMethodView):

  async def get(self, request):
      return text('I am async get method')

app.add_route(SimpleAsyncView.as_view(), '/')
```



## URL 参数

如果需要路由指南中讨论的任何URL参数，请将其包括在方法定义中。

```
class NameView(HTTPMethodView):

  def get(self, request, name):
    return text('Hello {}'.format(name))

app.add_route(NameView.as_view(), '/<name>')
```



## 装饰器

如果你想要添加任何装饰器到类，你可以设置 `decorators` 类的变量。这些会在 `as_view` 被调用时应用到类。

```
class ViewWithDecorator(HTTPMethodView):
  decorators = [some_decorator_here]

  def get(self, request, name):
    return text('Hello I have a decorator')

  def post(self, request, name):
    return text("Hello I also have a decorator")

app.add_route(ViewWithDecorator.as_view(), '/url')
```

但是如果你只想装饰一些函数而不是所有，你可以操作如下：

```
class ViewWithSomeDecorator(HTTPMethodView):

    @staticmethod
    @some_decorator_here
    def get(request, name):
        return text("Hello I have a decorator")

    def post(self, request, name):
        return text("Hello I don't have any decorators")
```



## URL 构建

如果你希望为 HTTPMethodView 构建 URL，记住类名将成为你传入 `url_for` 的端点。例如：

```
@app.route('/')
def index(request):
    url = app.url_for('SpecialClassView')
    return redirect(url)


class SpecialClassView(HTTPMethodView):
    def get(self, request):
        return text('Hello from the Special Class View!')


app.add_route(SpecialClassView.as_view(), '/special_class_view')
```



## 使用 CompositionView

作为 `HTTPMethodView` 的替代方案，你可用 `CompositionView` 在视图类之外移动处理函数。

每个支持的 HTTP 方法的处理程序都在源文件的其他地方定义了，然后使用 `CompositionView.add` 方法添加到视图。第一个参数是一个要处理的 HTTP 方法列表 (e.g. `['GET', 'POST']`)，第二个是处理程序。下面的例子展示了带两个外部处理程序和一个内部匿名函数的 `CompositionView` 的用法：

```
from sanic import Sanic
from sanic.views import CompositionView
from sanic.response import text

app = Sanic(__name__)

def get_handler(request):
    return text('I am a get method')

view = CompositionView()
view.add(['GET'], get_handler)
view.add(['POST', 'PUT'], lambda request: text('I am a post/put method'))

# Use the new view to handle requests to the base URL
app.add_route(view, '/')
```

注意：当前你不能通过 `url_for` 为 CompositionView 建立 URL。

# 自定义协议

*注意：这是高级用法，大部分读者用不到这功能。*

你可以通过指定一个继承于 [asyncio.protocol](https://docs.python.org/3/library/asyncio-protocol.html#protocol-classes) 的自定义的协议来修改 Sanic 协议的动作。该协议就可以作为关键字参数 `protocol` 被传递到 `sanic.run` 方法。

自定义协议类的构造函数从 Sanic 接收一下关键字参数。

- `loop`: 一个兼容 `asyncio` 的事件循环。
- `connections`: 一个保存协议对象的 `set`。当 Sanic 接收到 `SIGINT` 或 `SIGTERM`，会为所有保存在集合里协议执行 `protocol.close_if_idle`。
- `signal`: 一个带有 `stopped` 属性的 `sanic.server.Signal` 对象。当 Sanic 接收到 `SIGINT` 或 `SIGTERM`，`signal.stopped` 被置为 `True`。
- `request_handler`: 一个带着 `sanic.request.Request` 对象和 `response` 回调作为参数的协程。
- `error_handler`: 一个当异常抛出时回调的 `sanic.exceptions.Handler`。
- `request_timeout`: 请求超时秒数。
- `request_max_size`: 一个请求指定的最大数值，用 bytes。



## 例子

如果一个处理程序不返回 `HTTPResponse` 对象就会在默认协议引发错误。

通过复写 `write_response` 协议方法，当一个处理程序返回一个字符串它将转换成一个 `HTTPResponse`对象。

```
from sanic import Sanic
from sanic.server import HttpProtocol
from sanic.response import text

app = Sanic(__name__)


class CustomHttpProtocol(HttpProtocol):

    def __init__(self, *, loop, request_handler, error_handler,
                 signal, connections, request_timeout, request_max_size):
        super().__init__(
            loop=loop, request_handler=request_handler,
            error_handler=error_handler, signal=signal,
            connections=connections, request_timeout=request_timeout,
            request_max_size=request_max_size)

    def write_response(self, response):
        if isinstance(response, str):
            response = text(response)
        self.transport.write(
            response.output(self.request.version)
        )
        self.transport.close()


@app.route('/')
async def string(request):
    return 'string'


@app.route('/1')
async def response(request):
    return text('response')

app.run(host='0.0.0.0', port=8000, protocol=CustomHttpProtocol)
```

# SSL 例子

可以传入 SSLContext:

```
import ssl
context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain("/path/to/cert", keyfile="/path/to/keyfile")

app.run(host="0.0.0.0", port=8443, ssl=context)
```

你也可以用字典传入一个证书和密钥的位置：

```
ssl = {'cert': "/path/to/cert", 'key': "/path/to/keyfile"}
app.run(host="0.0.0.0", port=8443, ssl=ssl)
```

# 日志

Sanic 允许你在基于 [python3 logging API](https://docs.python.org/3/howto/logging.html) 的请求上做不同类型的日志 (access log, error log)。如果你想创建一个新的配置，你应该了解 python3 日志模块的基本知识。



## 快速开始

一个使用默认设置的简单例子如下：

```
from sanic import Sanic

app = Sanic('test')

@app.route('/')
async def test(request):
    return response.text('Hello World!')

if __name__ == "__main__":
  app.run(debug=True, access_log=True)
```

要使用你自己的日志配置，简单使用 `logging.config.dictConfig`，或者在你初始化 `Sanic` 应用的时候传递 `log_config`：

```
app = Sanic('test', log_config=LOGGING_CONFIG)
```

要关闭日志，只需指定 access_log=False:

```
if __name__ == "__main__":
  app.run(access_log=False)
```

这会在处理请求时跳过调用日志记录程序。并且你甚至可以在生产中进一步提高速度：

```
if __name__ == "__main__":
  # disable debug messages
  app.run(debug=False, access_log=False)
```



## 配置

默认情况下，log_config 参数设置为使用 sanic.log.LOGGING_CONFIG_DEFAULTS 字典进行配置。

sanic 使用了三种 `loggers`，并且 **当你想要创建你自己的日志配置时必须被定义**:

- root:
  用来记录内部消息。
- sanic.error:
  用来记录错误日志。
- sanic.access:
  用来记录访问日志。



### 日志格式化：

除了 python 提供的默认参数 (asctime, levelname, message) 外，Sanic 提供了额外的参数给访问日志：

- host (str)
  request.ip

- request (str)
  request.method + " " + request.url

- status (int)
  response.status

- byte (int)
  len(response.body)

默认的访问日志格式如下：

```
%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d
```

# 测试

Sanic 端可以使用 `test_client` 对象进行本地测试，该对象基于额外的 [aiohttp](https://aiohttp.readthedocs.io/en/stable/) 库。

`test_client` 公开 `get`, `post`, `put`, `delete`, `patch`, `head` 和 `options` 方法供你针对你的应用程序运行。一个简单的例子 (using pytest) 如下：

```
# Import the Sanic app, usually created with Sanic(__name__)
from external_server import app

def test_index_returns_200():
    request, response = app.test_client.get('/')
    assert response.status == 200

def test_index_put_not_allowed():
    request, response = app.test_client.put('/')
    assert response.status == 405
```

在内部，每次你调用 `test_client` 方法的任一，Sanic 会在 `127.0.0.1:42101` 执行并且你的测试请求会使用 `aiohttp` 针对你的应用程序进行执行。

`test_client` 方法接收如下参数和关键字参数：

- `uri` *(默认 '/')* 一个要测试的 URI 字符串。
- `gather_request` *(默认 True)* 一个确定是否被函数返回原始请求的布尔值。如果设置为 `True`，返回值十一个 `(request, response)` 的元组，如果是 `False` 就只返回响应。
- `server_kwargs` *(默认 {})* 一个在测试请求执行之前传入 `app.run` 的额外参数的字典。
- `debug` *(默认 False)* 一个确定是否在调试模式启动服务的布尔值。

程序进一步采用 `*request_args` 和 `**request_kwargs`，它们直接传递给 aiohttp ClientSession 请求。

例如，要提供数据给一个 GET 请求，你可以操作如下：

```
def test_get_request_includes_data():
    params = {'key1': 'value1', 'key2': 'value2'}
    request, response = app.test_client.get('/', params=params)
    assert request.args.get('key1') == 'value1'
```

要提供数据给一个 JSON POST 请求：

```
def test_post_json_request_includes_data():
    data = {'key1': 'value1', 'key2': 'value2'}
    request, response = app.test_client.post('/', data=json.dumps(data))
    assert request.json.get('key1') == 'value1'
```

更多关于 aiohttp 有效参数的信息可以在 [in the documentation for ClientSession](https://aiohttp.readthedocs.io/en/stable/client_reference.html#client-session) 找到。



## pytest-sanic

[pytest-sanic](https://github.com/yunstanford/pytest-sanic) 十一个 pytest 插件，它帮助你异步地测试你的代码。写法如下：

```
async def test_sanic_db_find_by_id(app):
    """
    Let's assume that, in db we have,
        {
            "id": "123",
            "name": "Kobe Bryant",
            "team": "Lakers",
        }
    """
    doc = await app.db["players"].find_by_id("123")
    assert doc.name == "Kobe Bryant"
    assert doc.team == "Lakers"
```

[pytest-sanic](https://github.com/yunstanford/pytest-sanic) 还提供了一些有用的装置，如 loop, unused_port, test_server, test_client。

```
@pytest.yield_fixture
def app():
    app = Sanic("test_sanic_app")

    @app.route("/test_get", methods=['GET'])
    async def test_get(request):
        return response.json({"GET": True})

    @app.route("/test_post", methods=['POST'])
    async def test_post(request):
        return response.json({"POST": True})

    yield app


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app, protocol=WebSocketProtocol))


#########
# Tests #
#########

async def test_fixture_test_client_get(test_cli):
    """
    GET request
    """
    resp = await test_cli.get('/test_get')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"GET": True}

async def test_fixture_test_client_post(test_cli):
    """
    POST request
    """
    resp = await test_cli.post('/test_post')
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json == {"POST": True}
```

# 部署

部署 Sanic 由内建的 web 服务器简化。在定义一个 `sanic.Sanic` 实例后，我们可以使用如下关键字参数调用 `run` 方法：

- `host` *(默认 "127.0.0.1")*: 主机服务器地址。
- `port` *(默认 8000)*: 主机服务器端口。
- `debug` *(默认 False)*: 启动调试输出 (减缓服务器速度).
- `ssl` *(默认 None)*: 为工作进程的 SSL 加密的 `SSLContext`。
- `sock` *(默认 None)*: 服务器接受连接的套接字。
- `workers` *(默认 1)*: 产生的工作进程的数量。
- `loop` *(默认 None)*: 一个兼容 `asyncio` 的事件循环。如果 none 被指定，Sanic 会建立自己的事件循环。
- `protocol` *(默认 HttpProtocol)*: [asyncio.protocol](https://docs.python.org/3/library/asyncio-protocol.html#protocol-classes) 的继承。



## 工作进程

默认情况下，Sanic 使用一个 CPU 核心在主程序中监听。为了加速，只需在 `run` 参数里指定 workers 工作进程的数量。

```
app.run(host='0.0.0.0', port=1337, workers=4)
```

Sanic 会自动启动多个进程并且在它们之间路由流量。我们建议尽可能多得根据你有的 CPU 核心数量。



## 在终端运行

如果你喜欢使用命令行参数，你可以通过执行这个模块启动一个 Sanic 服务。例如，如果你在一个名叫 `server.py` 文件里初始化了一个叫做 `app` 的 Sanic 应用，你可以运行服务如下：

```
python -m sanic server.app --host=0.0.0.0 --port=1337 --workers=4
```

这种运行 sanic 的方式，不需要在你的 Python 文件中调用 `app.run`。如果你这样做了，确保包装了它以便它只在解释器运行时执行。

```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, workers=4)
```



## 在 Gunicorn 运行

[Gunicorn](http://gunicorn.org/) ‘Green Unicorn’ 是一个 UNIX 下的 WSGI HTTP 服务器。这是一个从 Ruby 的 Unicorn 项目移植过来的预分叉工作者模型。

为了用 Gunicorn 运行 Sanic 应用程序，你需要为 Gunicorn `worler-class` 参数使用特定的 `sanic.worker.GunicornWorker`：

```
gunicorn myapp:app --bind 0.0.0.0:1337 --worker-class sanic.worker.GunicornWorker
```

如果你的应用程序遭受内存泄漏，你可以将 Gunicorn 配置为在处理完指定数量的请求后正常重启工作程序。这是一种便利的方法来帮助限制内存泄漏的影响。

查看 [Gunicorn Docs](http://docs.gunicorn.org/en/latest/settings.html#max-requests) 获取更多信息。



## 异步支持

如果你 *需要* 分享 sanic 进程给其他应用程序，特别是 `loop`，这非常合适。但是请注意，此方法不支持使用多个进程，并且一般来说这不是最佳运行应用的方式。

这是一个不完整的例子 (请参考示例中的 `run_async.py` 以获取更实用的内容)：

```
server = app.create_server(host="0.0.0.0", port=8000)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(server)
loop.run_forever()
```

# 扩展

社区创建的 Sanic 扩展列表。

- [Sanic-Plugins-Framework](https://github.com/ashleysommer/sanicpluginsframework): 为轻松创建和使用 Sanic 插件的库。
- [Sessions](https://github.com/subyraman/sanic_session): 支持 Session。允许使用 redis, memcache 或者内存存数。
- [CORS](https://github.com/ashleysommer/sanic-cors): 一个 flask-cors 移植项目。
- [Compress](https://github.com/subyraman/sanic_compress): 逊于你轻松地 gzip Sanic 响应。一个 Flask-Compress 的移植项目。
- [Jinja2](https://github.com/lixxu/sanic-jinja2): 支持 Jinja2 模板.
- [Sanic JWT](https://github.com/ahopkins/sanic-jwt): 为 Sanic 提供认证, JWT 和 权限作用域。
- [OpenAPI/Swagger](https://github.com/channelcat/sanic-openapi): OpenAPI 支持，加了 Swagger UI。
- [Pagination](https://github.com/lixxu/python-paginate): 简单的分页支持。
- [Motor](https://github.com/lixxu/sanic-motor): 简单的 motor 包装。
- [Sanic CRUD](https://github.com/Typhon66/sanic_crud): 使用 peewee 模型的 CRUD REST API 生成器。
- [UserAgent](https://github.com/lixxu/sanic-useragent): 添加 `user_agent` 到请求。
- [Limiter](https://github.com/bohea/sanic-limiter): sanic 的速率限制。
- [Sanic EnvConfig](https://github.com/jamesstidard/sanic-envconfig): 拉取环境变量到你的 sanic 配置。
- [Babel](https://github.com/lixxu/sanic-babel): 在 `Babel` 库的帮助下添加 i18n/l10n 支持到 Sanic 应用程序
- [Dispatch](https://github.com/ashleysommer/sanic-dispatcher): 一个在 werkzeug 受 `DispatcherMiddleware` 启发的调度。可以作为一个 Sanic-to-WSGI 适配器使用。
- [Sanic-OAuth](https://github.com/Sniedes722/Sanic-OAuth): 为连接或者创建你自己的 token 提供商的 OAuth 库
- [sanic-oauth](https://gitlab.com/SirEdvin/sanic-oauth): 拥有许多提供商的 OAuth 库并且支持 OAuth1/OAuth2。
- [Sanic-nginx-docker-example](https://github.com/itielshwartz/sanic-nginx-docker-example): 简单轻松地在 docker-compose 的 nginx 后使用 Sanic 示例。
- [sanic-graphql](https://github.com/graphql-python/sanic-graphql): GraphQL 与 Sanic 的集成。
- [sanic-prometheus](https://github.com/dkruchinin/sanic-prometheus): Sanic 的 Prometheus 指标。
- [Sanic-RestPlus](https://github.com/ashleysommer/sanic-restplus): 为 Sanic 移植的 Flask-RestPlus。带 SwaggerUI 生成器的全功能 REST API。
- [sanic-transmute](https://github.com/yunstanford/sanic-transmute): 一个 Sanic 扩展，从 python 的函数和类中生成 APIs，而且还自动生成 Swagger UI/文档。
- [pytest-sanic](https://github.com/yunstanford/pytest-sanic): Sanic 的 pytest 插件。它帮助你异步地测试你的代码。
- [jinja2-sanic](https://github.com/yunstanford/jinja2-sanic): Sanic 的 jinja2 模板渲染库。([Documentation](http://jinja2-sanic.readthedocs.io/en/latest/))
- [GINO](https://github.com/fantix/gino): 一个在 SQLAlchemy 核心上的异步 ORM，随 Sanic 扩展一起交付。 ([Documentation](https://python-gino.readthedocs.io/))
- [Sanic-Auth](https://github.com/pyx/sanic-auth): Sanic 的最小后端不可知的基于会话的用户认证机制。
- [Sanic-CookieSession](https://github.com/pyx/sanic-cookiesession): 仅基于cookie的客户端会话，类似于Flask中的内置会话。
- [Sanic-WTF](https://github.com/pyx/sanic-wtf): Sanic-WTF 使得使用带有 Sanic 和 CSRF (Cross-Site Request Forgery) 的 WTForms 更容易一些。

# 贡献

谢谢你的关注！Sanic 一直在寻找贡献这。如果你不习惯贡献代码，那么向源文件中添加文档是非常值得赞赏的。



## 安装

要开发sanic（主要是为了运行测试），强烈建议从源代码安装。

所以假设你已经克隆了repo，并且已经在已经设置了虚拟环境的工作目录中，然后运行：

```
python setup.py develop && pip install -r requirements-dev.txt
```



## 运行测试

要运行 sanic 的测试，强烈建议使用 tox 如下：

```
tox
```

看就这么简单！



## Pull requests!

pull request 批准规则非常简单：

1. 所有 pull requests 必须通过测试

- 所有 pull requests 必须至少被项目中的一名当前合作者
- 所有 pull requests 必须通过 flake8 检查
- 如果你决定从任何公共接口中 删除/修改 任何内容，则应附上该消息。
- 如果你执行一个新的功能你应该至少有意个单元测试来附上它。



## 文档

Sanic 的文档使用 [sphinx](http://www.sphinx-doc.org/en/1.5.1/) 建立。指南用 Markdown 协程，并且能在 `docs` 目录中找到，这个模块参考由 `sphinx-apidoc` 自动生成。

要从头生成文档：

```
sphinx-apidoc -fo docs/_api/ sanic
sphinx-build -b html docs docs/_build
```

HTML 文档会在 `docs/_build` 目录创建。



## 警告

Sanic 的主要目标之一是速度。代码可能会降低 Sanic 的性能，但在可用性，安全性或功能方面没有显着提升，可能不会合并。请不要被这吓到！如果您对某个想法有任何疑虑，开个 issue 来讨论和帮助吧。

# API Reference

## Submodules

## sanic.app module

## sanic.blueprints module

## sanic.config module

## sanic.constants module

## sanic.cookies module

## sanic.exceptions module

## sanic.handlers module

## sanic.log module

## sanic.request module

## sanic.response module

## sanic.router module

## sanic.server module

## sanic.static module

## sanic.testing module

## sanic.views module

## sanic.websocket module

## sanic.worker module

## Module contents