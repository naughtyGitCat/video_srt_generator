from utils.config import CONFIG, init_config
from utils.logger import get_logger
from utils.file import get_files

if CONFIG is None:
    CONFIG = init_config()
