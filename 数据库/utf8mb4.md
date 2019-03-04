mysql 5.5.3版本后增加了utf8mb4 编码。mb4 ---- most bytes 4。

MySQL的utf8是UTF-8的不完全实现，最大三字节的Unicode字符。

java驱动会自动检测服务端character_set_server的配置，如果为utf8mb4，驱动在建立连接的时候设置SET NAMES utf8mb4。然而其他语言没有依赖于这样的特性。









http://101.200.155.227:8080/im/webservice/imrest/backService/{api_key}/{ent_id}/depart?

http://101.200.155.227:8080/im/webservice/imrest/backService/{api_key}/{ent_id}/depart/{depart_no}?

http://101.200.155.227:8080/im/webservice/imrest/backService/{api_key}/{ent_id}/{depart_no}/depart?

平台请求IM接口前对参数进行了封装，统一使用utf8编码格式。

从同步用户可以看出请求前对数据的封装都是正确的，因为同步部门也是调用了sendRequestJSON这个方法。

平台同步部门和同步用户的逻辑是一样的，先反初始化，再初始化。

反初始化接收到IM的返回消息是该部门已删除，此时我查询数据库IMDepart表的信息并没有变化。

所以再进行初始化时返回消息是部门已经存在。





