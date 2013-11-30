import logging
from rallycaster import app


def set_configuration():
    app.logger.setLevel(logging.DEBUG)

    app.config.from_object('rallycaster.default_settings')
    app.config.from_pyfile('rallycaster.cfg')
