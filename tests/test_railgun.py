#coding: utf-8

import os
import sys
import shutil
import requests


root_path = os.getcwd()
test_env = os.path.join(root_path, 'tests/')
blog_path = os.path.join(test_env, 'blog/')

# build tree
build_tree = ['./blog/',
              './blog/app', './blog/gen',
              './blog/app/pages', './blog/app/themes', './blog/app/static', './blog/app/templates', 
              './blog/app/static/img', './blog/app/static/css', './blog/app/static/js', './blog/app/themes/cat',
              './blog/app/themes/cat/static', './blog/app/themes/cat/templates', 
              './blog/app/themes/cat/static/img', './blog/app/themes/cat/static/css', './blog/app/themes/cat/static/js']

def clean_test_env():
    shutil.rmtree(blog_path)
    print("\n>> clean test environment\n")

def test_railgun_init():
    if os.path.isdir(blog_path):
        shutil.rmtree(blog_path)
    os.chdir(test_env)
    print("\n>> build test environment\n")
    os.popen('railgun init blog')
    path_list = []
    for path, _, _ in os.walk("./blog/"):
        if "./blog/app/themes/cat/.git" not in path:
            path_list.append(path)
    assert set(path_list) == set(build_tree)

def test_railgun_new():
    os.chdir(blog_path)
    os.popen('railgun new test')
    new_blog_path = os.path.join(blog_path, 'app/pages/test.md')
    assert os.path.isfile(new_blog_path) == True

def test_railgun_build():
    os.chdir(blog_path)
    os.popen('railgun build')
    build_path = os.path.join(blog_path, 'app/build')
    build_test_path = os.path.join(build_path, 'test/')
    assert os.path.isdir(build_test_path)

# def test_railgun_server():
#     os.chdir(blog_path)
#     os.popen('railgun server')
#     r = requests.get('http://127.0.0.1:5050/')
#     assert r.status == '200'
#     clean_test_env()

def test_railgun_upload():
    os.chdir(blog_path)
    os.popen('railgun upload')
    harbor_path = os.path.join(blog_path, '.harbor/.git')
    assert os.path.isdir(harbor_path) 
    clean_test_env()
