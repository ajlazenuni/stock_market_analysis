# src/utils/logger.py
import logging
import os
from datetime import datetime


class Logger:
    def __init__(self):
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    f"{log_dir}/stock_market_{datetime.now().strftime('%Y%m%d')}.log"
                ),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)