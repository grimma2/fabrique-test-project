import logging
import logging.handlers
from pathlib import Path


def setup_loggers(BASE_DIR: Path):
    log_files = ['clients.log', 'mailings.log', 'messages.log']
    log_names = ['clientsLogger', 'mailingsLogger', 'messagesLogger']

    for log_name, log_file in zip(log_names, log_files):
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler(BASE_DIR.parent / 'logs' / log_file, mode='w')
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
