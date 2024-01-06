from structlog import *  # noqa F403

from kilmlogger.config import load_default_configuration
from kilmlogger.correlation import CorrelationIdMiddleware


__version__ = "0.0.5"
