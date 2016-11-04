title: ship api document
date: 2016-06-17 21:21:21
tags: ['ship', 'api']

[ship 文档](https://neo1218.github.io/ship)

# API文档
## ship-cli API
**ship init sitename**

    :param sitename: 站点的名称
    在当前目录下新建一个名为sitename的站点, 并集成默认主题, 开启dev server.
    如果已存在名为sitename的目录则终止创建的过程并提出警告.

**ship server**

    启动开发服务器, 进行本地预览

**ship new title**

    :param title: 文章文件名
    在{site}/app/pages/目录下创建一个title.md的文件(后缀名参考配置),
    文件内容自动填入下列信息

    title: 文章标题
    date: 2016-07-17 21:21:21 日期(自动生成)
    tags: ['tag1', 'tag2'] 标签

**ship build**

    全站静态化到{site}/app/build/目录

**ship upload**

    一键部署到git pages, 前提是[deploy on github/(git) pages]配置正确.

**ship upgrade themename**

    :param themename: 主题名称
    切换主题: 首先clone主题到{site}/app/themes/themename, 然后使用ship upgrade
    themename集成主题.

**ship status**

## ship-site API
### user_config_dict

    'ARTICLE_PER_PAGE': 平均每页文章数
    'SITE_NAME': 站点名称
    'SITE_URL': 站点url
    'SITE_DESC': 站点描述
    'SITE_OWNER': 站点作者
    'GITHUB_URL': github
    'WEIBO_URL': 微博
    'TWITTER_URL': twitter

### api_dict

    'posts': 所有pages下文章列表
    'posts_sum': 文章的总数目
    'latests': 所有文章列表按最近生成时间排序
    'tags': 所有标签列表
    'archive': 所有归档列表
