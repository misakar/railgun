# coding: utf-8
"""
    railgun::cli::operators::_mkdir_p.py
    `````````````````````````````````````

    act as mkdir function, ignore path exist

    :License :: MIT
    :Copyright @neo1218 2016
"""

import os, errno


def _mkdir_p(abspath):
    """
    :function _mkdir_p:
        act as mkdir function, but ignore path exist
    :param abspath: directory abs path
    """
    try:
        os.makedirs(abspath)
    except OSError as e:
        if (e.errno == errno.EEXIST) and (os.path.isdir(abspath)):
            pass
        else: raise
