import logging
import sys

from .helpers import T_STRING_AVAILABLE

class Logger:
    def __init__(self, verbose_level=0):
        self.verbose_level = verbose_level
        log_level = [logging.WARNING, logging.INFO, logging.DEBUG][min(verbose_level, 2)]
        logging.basicConfig(
            level=log_level,
            format='%(levelname)s: %(message)s',
            stream=sys.stdout
        )
        self.logger = logging.getLogger(__name__)

    def _format_msg(self, template, **kwargs):
        if T_STRING_AVAILABLE:
            return str(template)
        return template.s.format(**kwargs)

    def info(self, template, **kwargs):
        if self.verbose_level >= 1:
            if self.verbose_level >= 2:
                print(f"Template: {template!r}, kwargs: {kwargs!r}")
            self.logger.info(self._format_msg(template, **kwargs))

    def error(self, template, **kwargs):
        self.logger.error(self._format_msg(template, **kwargs))
