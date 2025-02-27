import logging
import logging.config
import logging.handlers
from pathlib import Path
from typing import Optional

class LoggerManager:
  """
  A singleton class to manage and configure logging for the entire system.
  
  Features:
    - Optionally load an external configuration file (INI format via fileConfig)
    - Default configuration includes:
      • Console handler (DEBUG and above)
      • Rotating file handler (INFO and above) with file rotation & retention
    - Provides a get_logger() method for consistent logger access across modules
  """
  _instance: Optional['LoggerManager'] = None

  def __new__(cls, config_file: Optional[str] = None) -> 'LoggerManager':
    if cls._instance is None:
      cls._instance = super(LoggerManager, cls).__new__(cls)
      cls._instance._initialized = False
    return cls._instance

  def __init__(self, config_file: Optional[str] = None) -> None:
    if self._initialized:
      return
    self._initialized = True

    if config_file and Path(config_file).exists():
      logging.config.fileConfig(config_file, disable_existing_loggers=False)
    else:
      self._configure_default()

  def _configure_default(self) -> None:
    """
    Configure logging with a default setup:
      - A console handler that prints all messages (DEBUG and above) with a simple format.
      - A rotating file handler that logs INFO and higher messages to 'app.log'
      (rotating when the file size exceeds 10MB, keeping 5 backup files).
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)

    file_handler = logging.handlers.RotatingFileHandler(
      "app.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

  def get_logger(self, name: str) -> logging.Logger:
    """
    Returns a logger with the specified name.
    This method should be used throughout your system so that all modules use a consistent logging configuration.
    """
    return logging.getLogger(name)


# ------------------ Example Usage ------------------
if __name__ == "__main__":
  log_manager = LoggerManager()  # or LoggerManager('logging.conf') if you have one

  logger = log_manager.get_logger(__name__)

  logger.debug("This is a DEBUG message - visible only on the console.")
  logger.info("This is an INFO message - logged to both console and file.")
  logger.warning("This is a WARNING message - check for potential issues.")

  try:
    result = 10 / 0
  except ZeroDivisionError as e:
    logger.error("An error occurred while performing division.", exc_info=True)
