import asyncio
import random
import sys
from loguru import logger


class Logger:
    def __init__(self, client_address = None):
        # self.client_address = client_address
        self.logger = logger.bind()
        self.logger_settings()

    def logger_settings(self):
        self.logger.remove()
        self.logger.add(sys.stdout, format=self.format_record, colorize=True)

    @staticmethod
    def format_record(record):
        logger_format = (
            "<green>{time}</green> - <green>{module}.{function}</green> - <level>"
            "{level}</level> - <cyan>Address: </cyan>"
        )
        if record["level"].name == "ERROR":
            logger_format += "<red> - {message}</red>\n"
        else:
            logger_format += " - {message}\n"
        return logger_format


async def sleep(a=3, b=None):
    if not b:
        await asyncio.sleep(a)
    else:
        sleep_for = random.randint(a, b)
        await asyncio.sleep(sleep_for)
