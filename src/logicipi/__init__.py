"""
Augmented structured logging for Python running on GCP
"""

from logicipi.function import Logger as gcp_logger
from logicipi.structlog import configure_structlog

__title__ = "logicipi"

__all__ = [
    "gcp_logger",
    "configure_structlog",
]
