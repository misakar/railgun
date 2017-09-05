# coding: utf-8

"""
    manage.py
    ~~~~~~~~~
"""

import os
import sys
import shutil
import platform
from app import app
from gen import Gen
from flask_script import Manager


"""编码设置"""
if (platform.python_version().split('.')[0] == '2'):
    # reload(sys) is evil :)
    reload(sys)
    sys.setdefaultencoding('utf-8')


"""Git配置"""
git_url = app.config['GIT_URL']
git_branch = app.config['BRANCH']


manager = Manager(app)


def first_upload():
    if not git_url:
        raise
    else:
        harbor_folder = os.path.join(os.getcwd(), '.harbor')
        os.chdir(harbor_folder)
        os.popen('git checkout -b %s' % git_branch)
        os.popen('git pull %s %s' % (git_url, git_branch))
        os.popen('git add .')
        os.popen('git commit -m "railgun site update...✅ "')
        os.popen('git push -u %s %s' % (git_url, git_branch))


def other_upload():
    if not git_url:
        raise
    else:
        harbor_folder = os.path.join(os.getcwd(), '.harbor')
        os.chdir(harbor_folder)
        os.popen('git checkout %s' % git_branch)
        os.popen('git add .')
        os.popen('git commit -m "railgun site update...✅ "')
        os.popen('git push -u %s %s' % (git_url, git_branch))


def update_static_res():
    static_folder = os.path.join(os.getcwd(), 'app/static')
    static_build_folder = os.path.join(os.getcwd(), 'app/build/static')
    if os.path.isdir(static_build_folder):
        shutil.rmtree(static_build_folder)
    shutil.copytree(static_folder, static_build_folder)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        _gen = Gen(app)
        _gen.gen()
        # update static resources
        update_static_res()
    elif len(sys.argv) > 1 and sys.argv[1] == 'first_upload':
        first_upload()
    elif len(sys.argv) > 1 and sys.argv[1] == 'other_upload':
        other_upload()
    else:
        manager.run()
