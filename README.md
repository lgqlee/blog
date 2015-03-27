Blog for vincenting.com.

- - -

1. 使用 toml 作为配置文件格式.
2. 前端使用了 semantic 的 less 文件，同时使用了 coffee script.
3. 前端使用了 bower 进行第三方库管理.
3. 数据库使用 mongo，同时在 tornado 异步 server 的支持下，全部使用异步.
4. 将使用 Whoosh 作为搜索引擎.
5. 使用 nose 进行 python 的代码测试，同时建议使用 coverage 进行测试用例覆盖率检测.

### 开始开发

只支持 python 3.*

* 安装 python3 所需要的依赖 `pip3 install -r requirements.txt`
* `npm install`
* `for req in $(cat requirements.txt); do sudo pip install $req; done`
* `bower install && gulp prepare && gulp setup` 下载前端需要的第三方内容
* `gulp watch`
* `npm test` 对 python 进行测试

### todo

1. 发布前的按需打包
2. 很多很多的功能...
3. 增加命令行功能，包括添加管理员等等
4. 使用 watir 等工具生成所有可能出现的页面，然后对 css 进行未使用删除来压缩
5. 实现基于 motor 的 ORM，考虑在 ORM 层面增加软删除和物理删除支持（待实现 queryBuilder 和动态查询支持以及查询结果封装）
6. 考虑实现 commands，主要用于在请求结束后继续其他操作
