# rest API

## 简介

1. REST请求仍然是标准的HTTP请求，但是，除了GET请求外，POST、PUT等请求的body是JSON数据格式，请求的`Content-Type`为`application/json`；
2. REST响应返回的结果是JSON数据格式，因此，响应的`Content-Type`也是`application/json`。
3. REST规范定义了资源的通用访问格式，虽然它不是一个强制要求，但遵守该规范可以让人易于理解。

## method

| 动词   | 对应 | 数据库 |
| ------ | ---- | ------ |
| GET    | 查询 | select |
| POST   | 新增 | insert |
| PUT    | 更新 | update |
| DELETE | 删除 | delete |

