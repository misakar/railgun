# coding: utf-8
"""
    views.py
    ````````

    railgun-site routes API
"""

from . import app
from . import pages
from flask import render_template, request
from flask_flatpages import pygments_style_defs
from .paginate import _Pagination


""" User Config """
article_per_page = app.config.get('ARTICLE_PER_PAGE')
user_config_dict = {
        'ARTICLE_PER_PAGE': article_per_page,
        'SITE_NAME': app.config.get('SITE_NAME'),
        'SITE_URL': app.config.get('SITE_URL'),
        'SITE_DESC': app.config.get('SITE_DESC'),
        'SITE_OWNER': app.config.get('SITE_OWNER'),
        'GIT_URL': app.config.get('GIT_URL'),
        'GITHUB_URL': app.config.get('GITHUB_URL'),
        'WEIBO_URL': app.config.get('WEIBO_URL'),
        'TWITTER_URL': app.config.get('TWITTER_URL'), }
""""""


""" API """
posts = [p for p in pages if 'date' in p.meta]
latests = sorted(posts, key=lambda p: p.meta['date'], reverse=True)
api_dict = {
        'posts': posts,
        'posts_sum': len(posts),
        'latests': latests,
        'tags': [p.meta.get('tag') for p in latests],
        'archives': {}.fromkeys(
                   [str(p.meta.get('date'))[:-3] for p in latests]).keys(), }
""""""


@app.route('/')
def index():
    if article_per_page != 0:
        page = int(request.args.get('page') or 1)
        if isinstance(latests, list):
            _latests = _Pagination(latests, page, article_per_page)
            api_dict['latests'] = _latests
        return render_template('index.html', **dict(user_config_dict, **api_dict))
    else:
        return render_template('index.html', **dict(user_config_dict, **api_dict))


@app.route('/<path:path>/')
def post(path):
    post = pages.get_or_404(path)
    api_dict['post'] = post
    return render_template('post.html', **dict(user_config_dict, **api_dict))


@app.route('/archive/<string:year>/')
def archive(year):
    posts = [p for p in pages if year in \
            str(p.meta.get('date')[-3])]
    api_dict['posts'] = posts
    return render_template('archive.html', **dict(user_config_dict, **api_dict))


@app.route('/archives/')
def archives():
    return render_template('archives.html', **dict(user_config_dict, **api_dict))


@app.route('/tag/<string:tag>/')
def tag(tag):
    posts = [p for p in pages if tag in p.meta.get('tags', [])]
    api_dict['posts'] = posts
    return render_template('tag.html', **dict(user_config_dict, **api_dict))


@app.route('/tags/')
def tags():
    return render_template('tags.html', **dict(user_config_dict, **api_dict))


@app.route('/about/')
def about():
    return render_template('about.html', **dict(user_config_dict, **api_dict))

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs(app.config.get('HIGHLIGHT_THEME')), 200, {'Content-Type': 'text/css'}
