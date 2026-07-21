"""
Atlas logging.
"""

from __future__ import annotations

import logging

from core.config import config


logging.basicConfig(
    filename=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("atlas")