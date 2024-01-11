#!/usr/bin/env python3
"""
Return a log message obfuscated
"""
import re
from typing import List
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter logs with the filter_datum function"""
        log = super(RedactingFormatter, self).format(record)
        message = filter_datum(self.fields, self.REDACTION, log,
                               self.SEPARATOR)
        return message

def get_logger() -> logging.Logger:
    """Get a logger Object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setformatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream)
    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message obfuscated"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}', f'{i}={redaction}{separator}',
                         message)
    return message
