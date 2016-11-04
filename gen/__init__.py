#coding: utf-8

import os
import shutil
import collections
import werkzeug
# from app import app
try:
    from urllib import unquote
    from urlparse import urlsplit
except ImportError: # python3 ~
    from urllib.parse import urlsplit, unquote
from contextlib import contextmanager
from threading import Lock
from flask import url_for
try:
    unicode
except NameError:  # python3 ~
    unicode = str
    basestring = str

class Gen(object):
    """
    static generator class
    acts like flask extension
    """
    def __init__(self, app=None):
        self.url_gens = []
        self.init_app(app)

    def init_app(self, app):
        self.app = app
        if app:
            self.url_fors = UrlForGen(app)  # all url_for ?
            app.config.setdefault('GEN_OUT_DEST', 'build')
            app.config.setdefault('GEN_DEFAULT_MIMETYPE',
                                  'application/octet-stream')
            app.config.setdefault('GEN_BASE_URL', None)

    def register_url_gens(self, function):
        """注册机制->同时方便函数延迟调用"""
        self.url_gens.append(function)
        return function

    @property
    def root_path(self):
        """build root path"""
        return os.path.join(
            unicode(self.app.root_path),
            unicode(self.app.config['GEN_OUT_DEST'])
        )

    def gen(self):
        # if not os.path.isdir(self.root_path):
        #    os.makedirs(self.root_path)
        if os.path.isdir(self.root_path):
            shutil.rmtree(self.root_path) # 先用简单粗暴的方式
        os.makedirs(self.root_path)  # new a build path in each build process
        built_urls = set()  # 已经build过的url集合
        built_endpoints = set()  # 已经build过的endpoints
        for url, endpoint in self._gen_all_urls():
            built_endpoints.add(endpoint)
            if url in built_urls:
                continue
            built_urls.add(url)
            print "call for _build_file"
            filename = self._build_file(url)
        return built_urls

    def has_no_empty_params(self, rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    def _gen_all_urls(self):
        """
        run all generators and yield (url, endpoint) tuple
        """
        base_url_path = self._base_url_path()
        url_encoding = self.app.url_map.charset  # 'utf-8'
        url_gens = list(self.url_gens)
        # add iter_calls function
        url_gens += [self.app.url_map.iter_rules]
        url_gens += [self.url_fors.iter_calls]  # all app url_for!
        with self.app.test_request_context(base_url=base_url_path or None):
            for gen in url_gens:
                print url_gens
                for gend in gen():
                    if isinstance(gend, werkzeug.routing.Rule):
                        if self.has_no_empty_params(gend):
                            url = gend.rule
                            endpoint = gend.endpoint
                            values = gend.defaults or {}
                        else: continue
                    elif isinstance(gend, basestring):
                        url = gend
                        endpoint = None
                    else:
                        if isinstance(gend, collections.Mapping):
                            values = gend
                            endpoint = gen.__name__  # gen->generator function
                        else: # assume a tuple
                            endpoint, values = gend
                    url = url_for(endpoint, **values)  # 构造url
                    assert url.startswith(base_url_path), (
                        'url_for returned an URL %r not starting with '
                        'base_url_path %r. Bug in Werkzeug?'
                        % (url, base_url_path)
                    )
                    url = url[len(base_url_path):]
                    url = unquote(url)
                    parsed_url = urlsplit(url)
                    if parsed_url.scheme or parsed_url.netloc:
                        raise ValueError('External URLs not supported: ' + url)
                    url = parsed_url.path  # only need path
                    if not isinstance(url, unicode):
                        url = url.decode(url_encoding)
                    print "yield url, endpoint"
                    yield url, endpoint

    def _build_file(self, url):
        gen_client = self.app.test_client()
        base_url = self.app.config['GEN_BASE_URL']
        with conditional_ctx(self.url_fors, True):
            response = gen_client.get(url, follow_redirects=True,
                                      base_url=base_url)
        destination_path = self.urlpath_to_filepath(url)
        filename = os.path.join(self.root_path, *destination_path.split('/'))
        # 不需要 -> mimetype warning
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        static_data = response.data
        with open(filename, 'wb') as fd:
            # 与其打开一个文件进行内容判断
            # 不如直接删除之前的所有文件, 然后全部重新创建
            # 简单粗暴!
            fd.write(static_data)
        print "build file {file}".format(file=filename)
        response.close()
        return filename

    def urlpath_to_filepath(self, path):
        """
        convert a URL path like /admin/ to a file path like admin/index.html
        """
        if path.endswith('/'):
            path += 'index.html'
        assert path.startswith('/')  # 断言判断, path会加'/'
        return path[1:]

    def _base_url_path(self):
        baseurl = self.app.config['GEN_BASE_URL']
        return urlsplit(baseurl or '').path.rstrip('/')


class UrlForGen(object):
    def __init__(self, app):
        self.app = app
        self.calls = collections.deque()
        self._enabled = False
        self._lock = Lock()  # 上锁啦, 哈哈, 有意思

        def gens(endpoint, values):
            if self._enabled:
                self.calls.append((endpoint, values.copy()))
        self.app.url_default_functions.setdefault(None, []).insert(0, gens)
        # {None: [<function gens at xxxx>, <function logger at xxxx>]} only one

    def __enter__(self):
        # 任务管理器?
        self._lock.acquire()  # 上锁
        self._enabled = True

    def __exit__(self, exc_type, exc_value, traceback):
        self._enabled = False
        self._lock.release()  # 释放锁

    def iter_calls(self):
        while self.calls:  # 双端队列 [(endpoint, values)]
            yield self.calls.popleft()

@contextmanager
def conditional_ctx(context, condition):
    if condition:
        with context:
            yield
    else:
        yield  # yield
