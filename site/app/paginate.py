# coding: utf-8
"""
    ship::site::paginate.py

    posts resources pagination

    :License :: MIT
    :Copyright @neo1218 2016
"""

from collections import MutableSequence


class _Pagination(MutableSequence):
    """
    Pagination Class
    """
    def __init__(self, resources, current, per_page):
        super(_Pagination, self).__init__()
        self._resources = resources
        self._num = per_page
        self._sum = len(resources)
        self._pages = self._sum // self._num
        if self._sum % self._num != 0:
            self._pages += 1
        self._current = current
        self.prev_num = self._current-1 if self.has_prev() else None
        self.next_num = self._current+1 if self.has_next() else None

    def __len__(self):
        return len(self._resources)

    def __getitem__(self, i):
        return self._resources[i]

    def __setitem__(self, i, var):
        self._resources[i] = var

    def __delitem__(self, i):
        del self._resources[i]

    def insert(self, i, var):
        self._resources.insert(i, var)

    def append(self, var):
        self.insert(sef._sum, var)

    def has_prev(self):
        return True if self._current > 1 else False

    def has_next(self):
        return True if self._current < self._pages else False

    def __repr__(self):
        return "Pagination on %r" % self._resources
