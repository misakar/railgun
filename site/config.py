# coding: utf-8
"""
    config.py
    `````````

    railgun-site user config
"""


class Config(object):
    DEBUG = True
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = '.md'


class ExampleConfig(Config):
    # [site setting]
    SITE_NAME = "railgun site"
    SITE_URL = "https://neo1218.github.io"
    SITE_DESC = "a railgun site"
    SITE_OWNER = "neo1218"
    SITE_KEYWORDS = "railgun neo1218"

    # [article setting]
    ARTICLE_TYPE = FLATPAGES_EXTENSION = '.md'  # default is .md
    ARTICLE_PER_PAGE = 10

    # [owner info]
    GITHUB_URL = "https://github.com/neo1218"
    WEIBO_URL = "http://www.weibo.com/5551886705/profile"
    TWITTER_URL = "https://twitter.com/neo1218substack"
    QQ = "834597629"
    EMAIL = "neo1218@yeah.net"

    # [deploy on github/(git) pages]
    GIT_URL = "https://github.com/neo1218/ship"
    BRANCH = "gh-pages"
    GEN_BASE_URL = SITE_URL


class MyConfig(Config):
    # [site setting]
    SITE_NAME = ""
    SITE_URL = ""
    SITE_DESC = ""
    SITE_OWNER = ""
    SITE_KEYWORDS = ""

    # [article setting]
    ARTICLE_TYPE = FLATPAGES_EXTENSION = ".md"
    ARTICLE_PER_PAGE = 10

    # [owner info]
    GITHUB_URL = ""
    WEIBO_URL = ""
    TWITTER_URL = ""
    QQ = ""
    EMAIL = ""

    # [deploy on github/(git) pages]
    GIT_URL = ""
    BRANCH = ""
    GEN_BASE_URL = SITE_URL


config = {
    'default': ExampleConfig
}
