Blog for vincenting.com.

- - -

1. 使用 toml 作为配置文件格式.
2. 前端使用了 semantic 的 less 文件，同时使用了 coffee script.
3. 数据库使用 mongo，同时在 tornado 异步 server 的支持下，全部使用异步.
4. 将使用 Whoosh 作为搜索引擎.

### 开始开发

只支持 python 3.*

* `npm install`
* `gulp setup`
* `gulp watch`
* `nosetests ./tests --with-coverage -v`

### todo

1. 发布前的按需打包
2. 很多很多的功能...
3. 增加命令行功能，包括添加管理员等等
4. 使用 watir 等工具生成所有可能出现的页面，然后对 css 进行未使用删除来压缩