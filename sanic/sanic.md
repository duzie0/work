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