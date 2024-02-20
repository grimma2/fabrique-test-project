import time
import random
import logging
from dataclasses import dataclass, field

from .exceptions import MaxRetries, InvalidDataAnswer

import asyncio


@dataclass
class ExponentialBackoff:
    base_delay: int = field(default=2)
    max_retries: int = field(default=5)
    max_delay: int = field(default=60)

    async def delay(self, retry_count):
        """
        Вычисление задержки для текущей попытки.
        """
        delay = min(self.base_delay * (2 ** (retry_count - 1)), self.max_delay)
        # Случайное добавление времени для избежания одновременных повторных попыток
        jitter = random.uniform(0, self.base_delay)
        return delay + jitter

    async def execute_with_backoff(self, func, *args, **kwargs):
        for retry in range(1, self.max_retries + 1):
            try:
                return await func(*args, **kwargs)
            except InvalidDataAnswer as e:
                logging.error(f'InvalidDataAnswer: {e}')
                self.queue_message['retries'] += 1
                if retry == self.max_retries:
                    break
                else:
                    delay = await self.delay(retry)
                    logging.debug(f'deplay for {delay} seconds...')
                    await asyncio.sleep(delay)
    
        raise MaxRetries("Превышено максимальное количество попыток")
