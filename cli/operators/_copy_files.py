# coding: utf-8
"""
    railgun::cli::operators::_copy_files
    `````````````````````````````````````

    copy files from given path to {harbor} folder

    :License :: MIT
    :Copyright @neo1218 2016
"""

import os
import shutil
from ._mkdir_p import _mkdir_p


def _copy_files(path, harbor_folder):
    """
    :function _copy_files:
        copy files from given path to {harbor} folder
    :param path: build files path
    :param harbor_folder: harbor folder
    """
    for dirpath, sub_dirs, filenames in os.walk(path):
        relative = dirpath.split(path)[1].lstrip(os.path.sep)
        harbor_dir = os.path.join(harbor_folder, relative)

        _mkdir_p(harbor_dir)

        for filename in filenames:
            build_file = os.path.join(dirpath, filename)
            harbor_file = os.path.join(harbor_dir, filename)

            shutil.copy(build_file, harbor_file)
