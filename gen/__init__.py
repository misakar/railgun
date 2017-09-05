#coding: utf-8
"""
    gen
    ````

    static files generator for railgun

    :License: MIT
    :Copyright: @neo1218; @oaoouo
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
        self.gen_funcs= []
        self.init_app(app)

    def init_app(self, app):
        self.app = app
        if self.app:
            self.url_fors = UrlForGen(app)
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
            shutil.rmtree(self.root_path)
        os.makedirs(self.root_path)

        built_urls = set()
        built_endpoints = set()

        for url, endpoint in self._gen_all_urls():
            built_endpoints.add(endpoint)
            if url in built_urls:
                continue
            built_urls.add(url)

            destination_path = self.urlpath_to_filepath(url)
            filename = os.path.join(self.root_path, *destination_path.split('/'))
            dirname = os.path.dirname(filename)
            static_data = ""
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            for resp in self.wsgi_resquest(url):
                static_data += resp.data
            # write response to static files
            with open(filename, 'wb') as fd:
                fd.write(static_data)

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
        gen_funcs = self.gen_funcs
        # add iter_rules function
        gen_funcs += [self.app.url_map.iter_rules]
        # add iter_calls function
        gen_funcs += [self.url_fors.iter_calls]
        with self.app.test_request_context(base_url=base_url_path or None):
            # flask request context
            for func in gen_funcs:
                for _rule in func():
                    if isinstance(_rule, werkzeug.routing.Rule):
                        # iter_rules
                        if self.has_no_empty_params(_rule):
                            url = _rule.rule
                            endpoint = _rule.endpoint
                            values = _rule.defaults or {}
                    elif isinstance(_rule, basestring):
                        # iter_rules
                        url = _rule
                        endpoint = None
                    elif isinstance(_rule, collections.Mapping):
                        # iter_rules
                        values = _rule
                        endpoint = gen.__name__
                    else:
                        # iter_calls
                        endpoint, values = _rule
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

    def wsgi_resquest(self, url):
        """
        simulation request on WSGI level
        """
        gen_client = self.app.test_client()
        base_url = self.app.config['GEN_BASE_URL']
        with self.url_fors:
            response = yield gen_client.get(url, follow_redirects=True,
                                      base_url=base_url)

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
        self._lock = Lock()

        def gens(endpoint, values):
            """
            url processors can automatically inject values into a call for url_for() automatically.
            http://flask.pocoo.org/docs/0.11/patterns/urlprocessors/
            """
            if self._enabled \
            and ((endpoint, values) not in self.calls):
                self.calls.append((endpoint, values.copy()))
        # {None: [<function gens at xxxx>]}
        self.app.url_default_functions.setdefault(None, []).insert(0, gens)

    def __enter__(self):
        self._lock.acquire()
        self._enabled = True

    def __exit__(self, exc_type, exc_value, traceback):
        self._enabled = False
        self._lock.release()

    def iter_calls(self):
        while self.calls:
            yield self.calls.popleft()
