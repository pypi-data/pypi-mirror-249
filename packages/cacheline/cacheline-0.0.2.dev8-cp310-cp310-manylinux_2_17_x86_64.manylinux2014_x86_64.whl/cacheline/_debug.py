import logging
import sys
from typing import Optional


def setup_debug_hook():
    from better_exceptions import hook

    hook()


def setup_debug_logging(log_filepath: Optional[str] = None):
    import colorlog

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    for handler in root.handlers:
        root.removeHandler(handler)

    stream_handler = colorlog.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s %(reset)s%(pathname)s:%(lineno)d ",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={
                "message": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                }
            },
            style="%",
        )
    )
    root.addHandler(stream_handler)

    if log_filepath:
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - 🌟 %(message)s - %(pathname)s:%(lineno)d"
            )
        )
        root.addHandler(file_handler)


def enable_all_debugger():
    setup_debug_logging()
    setup_debug_hook()
