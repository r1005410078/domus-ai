import logging
import sys

def setup_logging():
    log_format = (
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)  # 输出到控制台
        ]
    )

setup_logging()
logger = logging.getLogger("app")

  