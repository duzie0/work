# 平台通用upload插件

## 1.简介

该插件为平台通用上传插件，依赖`jQuery`、`Bootstrap`、`uuid`、`sparkmd5`和平台的样式控制 。

**支持以下功能**

- 自定义参数
- 初始化已上传文件
- 模态框和内嵌两种显示形式
- 同一页面多个上传接口
- 单文件上传、单文件取消上传、单文件删除
- 批量上传、批量取消上传、批量删除
- 显示上传进度
- 下载已上传文件

## 2.插件使用

### 2.1 初始化

#### 2.1.1 引用`js`资源和设置插件唤醒按钮

使用该插件依赖`jQuery`、`Bootstrap`、`uuid`、`sparkmd5` ，平台已经导入`jQuery`和`Bootstarp`,只需再引入该插件的`js`资源和`uuid`,`sparkmd5`

````html
<script src="....sparkmd5.js"></script>
<script src="....uuid.js"></script>
<script src="....upload.js"></script>
````

设置插件唤醒按钮，需要添加`id`, 此`id` 也是下文中插件参数的`selector`

```html
<div >
    <button type="button" class="btn btn-primary" id="upload" >内嵌</button>
</div>
```

#### 2.1.2 初始化插件参数

```javascript
var general_upload = function initUpload(type,selector,name,showType){
    return generalUpload({
        type:type,
        selector: selector,
        showType: showType,
        name: name,
        upload:{
            url:'upload',
            lsize:[]，
            lnumber:[],
        	lftype:[".txt",".jpg",".png",".docx"],
            adata:{
                    "flowid"    :"",
                    "taskid"    :"",
                    "usercode"  :"",
                    "flag1"     :"",
                    "usercode"  :"",
                    "bindid"    :""
             }，
    		cal:function(){},//上传开始回调函数
            sCal:function(){},//上传成功回调
            eCal:function(){}//上传失败回调
		},
        delete:{
            url:'delfile?atta_id='
            cal:function(){},//删除开始回调函数
            sCal:function(){},//删除成功回调
            eCal:function(){}//删除失败回调
        },
        download:{
            url:'download?atta_id=',
            cal:function(){},//下载开始回调函数
            sCal:function(){},//下载成功回调
            eCal:function(){}//下载失败回调
        },
        style:{
            modal_top:25
        },
        init:{
            files_list:files_list，
            cal:function(){},//初始化开始回调函数
            sCal:function(){},//初始化成功回调
            eCal:function(){}//初始化失败回调
        }
   })
}；
var up = general_upload(type,selector,name,showType);
```

#### 2.2.3 参数说明

| 参数                 | 说明                                           | 类型    | 默认值               | NULL   |
| -------------------- | ---------------------------------------------- | ------- | -------------------- | ------ |
| `up.type`            | 1是正常的附件上传类型，2是平台节点附件更新类型 | number  | 1                    | 允许   |
| `up.selector`        | `css` 选择器语法                               | string  | 无默认值             | 不允许 |
| `up.showType`        | 1是模态框样式，2是内嵌样式                     | number  | 无默认值             | 不允许 |
| `up.name`            | 模态框 `header` 的标题                         | string  | 无默认值             | 不允许 |
| `up.upload.url`      | 上传路由接口                                   | string  | 无默认值             | 不允许 |
| `up.upload.lsize`    | 文件上传大小限制，单位B                        | object  | [0,Number.MAX_VALUE] | 允许   |
| `up.upload.lnumber`  | 文件上传数量限制                               | object  | [0,Number.MAX_VALUE] | 允许   |
| `up.upload.lftype`   | 文件上传类型限制                               | object  | []                   | 允许   |
| `up.upload.adata`    | 上传附带参数                                   | object  | {}                   | 允许   |
| `up.delete.url`      | 删除文件接口                                   | string  | 无默认值             | 不允许 |
| `up.download.url`    | 下载文件接口                                   | string  | 无默认值             | 不允许 |
| `up.style.modal_top` | 模态框初始位置                                 | number  | 15                   | 允许   |
| `up.init.files_list` | 初始化已上传的文件列表                         | object  | []                   | 允许   |
| `up.init.allow_del`  | 初始化文件是否允许删除                         | boolean | false                | 允许   |

## 3.注意事项

- 同一页面设置多个插件接口时，selector需要唯一标识
- `up.type` 设置为2 时只用在节点更新文件，且节点更新文件只对模态框形式有效
- `up.style.modal_top` 模态框初始位置（平台不同页面，模态框初始化位置不同，需要调试）
- `up.download.url` 下载路由接口，路由参数为`atta_id`（路由参数平台后台处理函数决定）
- `up.delete.url` 删除路由接口，路由参数为`atta_id`（路由参数平台后台处理函数决定）
- 可以通过访问插件的`up.files_num` 、`up.upload.wait_files`、`up.upload.now_files`和`up.upload.com_files`这些变量来查看插件上传的工作状态：
  - `up.upload.wait_files` 待上传列表
  - `up.upload.now_files`正在上传列表
  - `up.upload.com_files` 上传完成列表
  - `up.files_num`为插件内部参数，用于记录插件当前文件列表中文件的总数
- 插件载入浏览器完毕，之后添加的文件`checkbox`样式未受到平台样式影响，所以在插件内部引入了`App.initUniform();` ，插件`checkbox`样式依赖平台对页面样式的初始化。