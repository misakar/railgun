# ⚡️ railgun

> py static site generator

## Install

    $ pip install railgun-cli

## Config
you can modify site settings in [config.py](https://github.com/neo1218/railgun/blob/master/site/config.py)

### ⚡️ Site

Setting | Description
--- | ---
`SITE_NAME` | the name of your website
`SITE_URL` | your website url, important for path build
`SITE_DESC` | your website description
`SITE_OWNER` | your name...
`SITE_KEYWORDS` | the keyword description of your site

### ⚡️ Article

Setting | Description
--- | ---
`ARTICLE_TYPE` | article type, default is markdown
`ARTICLE_PER_PAGE` | The amount of the posts displayed on a single page. 0 disables pagination

### ⚡️ Owner

Setting | Description
--- | ---
`GITHUB_URL` | your github account
`WEIBO_URL` | your weibo account
`TWITTER_URL` | your twitter account
`QQ` | your QQ account
`EMAIL` | your email

### ⚡️ Deployment

Setting | Description
--- | ---
`GIT_URL`: github repo url
`BRANCH`: github repo branch, eg: master or gh-pages

> do not forget switch from ExampleConfig to MyConfig

```
config = {
    'default':  MyConfig
}
```

## Usage
railgun provided [railgun-commandline-tools](https://github.com/neo1218/railgun/blob/master/cli/railgun.py)

![railgun-cli](http://7xj431.com1.z0.glb.clouddn.com/屏幕快照 2016-11-05 上午12.45.34.png)

### ⚡️ railgun init

### ⚡️ railgun new

### ⚡️ railgun server

### ⚡️ railgun upgrade

### ⚡️ railgun build

### ⚡️ railgun deploy

## License
MIT, check [LICENSE](https://github.com/neo1218/railgun/blob/master/LICENSE) for detail.
