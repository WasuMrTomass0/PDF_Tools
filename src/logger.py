import logging
import traceback

import popup_windows
import settings
from language import Language

logger = logging.getLogger('logger')
fh = logging.FileHandler(settings.LOG_FILE_PATH)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(pathname)s : %(lineno)s - %(asctime)s\n\t%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def log_exceptions(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as error:
            logger.error(msg=f'{str(error)}\n{traceback.format_exc()}')
            popup_windows.error_popup(
                title=Language.error_unknown,
                msg=str(error)
            )

    return wrapper
