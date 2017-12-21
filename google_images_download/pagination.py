"""Pagination module."""


class Pagination(object):
    """Pagination obj."""

    def __init__(self, page, page_func=None):
        self.page = page
        self.page_func = page_func

    @property
    def has_prev(self):
        """Return True if it has previous page."""
        return self.page > 1

    @property
    def has_next(self):
        """Return True if it has next page."""
        return True

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Return page number."""
        pages = self.page
        last = 0
        for num in range(1, pages + 1):
            cond = num <= left_edge or (
                num > self.page - left_current - 1 and
                num < self.page + right_current
            ) or num > pages - right_edge
            if cond:
                if last + 1 != num:
                    yield None
                yield num
                last = num
