# coding: utf-8

"""
    manage.py
    ~~~~~~~~~
"""

import os
import shutil
import sys
from app import app
from gen import Gen
from flask_script import Manager


"""编码设置"""
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
        os.popen('git pull -u %s %s' % (git_url, git_branch))
        os.popen('git add .')
        os.popen('git commit -m "ship site update...✅ "')
        os.popen('git push -u %s %s' % (git_url, git_branch))


def other_upload():
    if not git_url:
        raise
    else:
        harbor_folder = os.path.join(os.getcwd(), '.harbor')
        os.chdir(harbor_folder)
        os.popen('git checkout %s' % git_branch)
        os.popen('git add .')
        os.popen('git commit -m "ship site update...✅ "')
        os.popen('git push -u %s %s' % (git_url, git_branch))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        _gen = Gen(app)
        _gen.gen()
    elif len(sys.argv) > 1 and sys.argv[1] == 'first_upload':
        first_upload()
    elif len(sys.argv) > 1 and sys.argv[1] == 'other_upload':
        other_upload()
    else:
        manager.run()
