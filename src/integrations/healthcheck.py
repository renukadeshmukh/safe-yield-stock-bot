import logging
import requests
from ..config import HEALTHCHECK_URL

logger = logging.getLogger(__name__)


def ping_health():
    """Ping healthcheck endpoint. Call on every heartbeat cycle."""
    if not HEALTHCHECK_URL:
        return
    try:
        requests.get(HEALTHCHECK_URL, timeout=5)
    except Exception as e:
        logger.warning(f"Health ping failed: {e}")


def ping_fail(reason: str = ""):
    """Signal failure to healthcheck endpoint."""
    if not HEALTHCHECK_URL:
        return
    try:
        requests.get(f"{HEALTHCHECK_URL}/fail", timeout=5)
    except Exception:
        pass
