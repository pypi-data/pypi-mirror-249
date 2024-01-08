import logging
import click
import sentry_sdk

from patched_cli.utils.managed_files import LOG_FILE

# default noop logger
logger = logging.getLogger("patched_cli")
_noop = logging.NullHandler()
logger.addHandler(_noop)


class ClickHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.addFilter(self._info_and_error_only)

    def emit(self, record: logging.LogRecord) -> None:
        is_error = record.levelno == logging.ERROR
        click.echo(record.message, err=is_error)
        if is_error:
            sentry_sdk.capture_exception(record.exc_info)

    @staticmethod
    def _info_and_error_only(record) -> int:
        return record.levelno == logging.INFO or record.levelno == logging.ERROR


def init_cli_logger() -> logging.Logger:
    global logger, _noop
    logger.removeHandler(_noop)

    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_FILE, mode="w")
    formatter = logging.Formatter("%(asctime)s :: %(filename)s@%(funcName)s@%(lineno)d :: %(levelname)s :: %(msg)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ClickHandler())

    return logger
