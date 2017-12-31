# coding: utf-8
"""
    railgun::cli::operators::_touch_file
    ````````````````````````````````````

    create file and init with template code

    :License :: MIT
    :Copyright @misakar
"""


def _touch_file(file_path, template):
    """
    :function _touch_file:
        crate file and init with template code
    :param file_path: file path
    :param template: template code:ship::cli::templates
    """
    with open(file_path, 'w+') as f:
        f.write(template)
