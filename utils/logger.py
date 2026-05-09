import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 创建 logger
logger = logging.getLogger("toutiao_backend")
logger.setLevel(logging.INFO)

# 控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# 文件处理器（自动轮转，最大10MB，保留5个备份）
file_handler = RotatingFileHandler(
    log_dir / "app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# 错误日志文件
error_handler = RotatingFileHandler(
    log_dir / "error.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(file_formatter)
logger.addHandler(error_handler)


def get_logger(name: str = None):
    """
    获取 logger 实例
    """
    if name:
        return logging.getLogger(f"toutiao_backend.{name}")
    return logger