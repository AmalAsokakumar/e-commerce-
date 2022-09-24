from jinja2.ext import Extension

from . import functions


class DjangoCompat(Extension):
    def __init__(self, environment):
        super(DjangoCompat, self).__init__(environment)

        environment.extend(
            now=functions.now,
        )
