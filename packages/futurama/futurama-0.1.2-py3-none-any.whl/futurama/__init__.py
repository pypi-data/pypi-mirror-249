from __future__ import annotations

import random

from .quotes import quotes


def get_random_futurama_quote() -> str:
    return random.choice(quotes)
