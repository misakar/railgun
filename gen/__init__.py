#coding: utf-8
"""
    gen
    ````

    static files generator for railgun

    :License: MIT
    :Copyright: @neo1218
"""

import os
import shutil
import collections
import werkzeug
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
    static files generator class
    """
    def __init__(self, app=None):
        self.url_gens = []
        self.init_app(app)

    def init_app(self, app):
        self.app = app
        if app:
            self.url_fors = UrlForGen(app)  # all url_for ?
            app.config.setdefault('GEN_OUT_DEST', 'build')
            app.config.setdefault('GEN_BASE_URL', None)

    def register_url_gens(self, function):
        """
        register url_gens function
        """
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
        """
        generator static files
        """
        if os.path.isdir(self.root_path):
            shutil.rmtree(self.root_path) # 简单粗暴⚡️
        os.makedirs(self.root_path)
        built_urls = set()
        built_endpoints = set()
        for url, endpoint in self._gen_all_urls():
            built_endpoints.add(endpoint)
            if url in built_urls:
                continue
            built_urls.add(url)
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
        # add iter_rules function
        url_gens += [self.app.url_map.iter_rules]
        # add iter_calls function
        url_gens += [self.url_fors.iter_calls]
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
                            endpoint = gen.__name__
                        else:
                            endpoint, values = gend
                    url = url_for(endpoint, **values)  # 构造url
                    assert url.startswith(base_url_path), (
                        'url_for returned an URL %r not starting with '
                        'base_url_path %r.'
                        % (url, base_url_path)
                    )
                    url = url[len(base_url_path):]
                    url = unquote(url)
                    parsed_url = urlsplit(url)
                    if parsed_url.scheme or parsed_url.netloc:
                        raise ValueError('External URLs not supported: ' + url)
                    url = parsed_url.path
                    if not isinstance(url, unicode):
                        url = url.decode(url_encoding)
                    yield url, endpoint

    def _build_file(self, url):
        """
        simulation request on WSGI level and
        write response to static files
        """
        gen_client = self.app.test_client()
        base_url = self.app.config['GEN_BASE_URL']
        with self.url_fors:
            # find all app url_for and build url
            response = gen_client.get(url, follow_redirects=True,
                                      base_url=base_url)
        destination_path = self.urlpath_to_filepath(url)
        filename = os.path.join(self.root_path, *destination_path.split('/'))
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        static_data = response.data
        with open(filename, 'wb') as fd:
            fd.write(static_data)
        print "build file {file}".format(file=filename)
        # response.close()
        return filename

    def urlpath_to_filepath(self, path):
        """
        convert a URL path like /admin/ to a file path like admin/index.html
        """
        if path.endswith('/'):
            path += 'index.html'
        assert path.startswith('/')
        return path[1:]

    def _base_url_path(self):
        baseurl = self.app.config['GEN_BASE_URL']
        return urlsplit(baseurl or '').path.rstrip('/')


class UrlForGen(object):
    """
    app url_for rules
    """
    def __init__(self, app):
        self.app = app
        self.calls = collections.deque()
        self._enabled = False
        self._lock = Lock()  # 上锁啦, 哈哈, 有意思

        def gens(endpoint, values):
            """
            ⚡️ 通过flask url processors获取所有url_for调用信息
            http://flask.pocoo.org/docs/0.11/patterns/urlprocessors/
            """
            if self._enabled:
                self.calls.append((endpoint, values.copy()))
        self.app.url_default_functions.setdefault(None, []).insert(0, gens)
        # {None: [<function gens at xxxx>]}

    def __enter__(self):
        self._lock.acquire()
        self._enabled = True

    def __exit__(self, exc_type, exc_value, traceback):
        self._enabled = False
        self._lock.release()

    def iter_calls(self):
        while self.calls:
            yield self.calls.popleft()
