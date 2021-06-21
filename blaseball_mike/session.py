import os
import atexit
import asyncio
from json.decoder import JSONDecodeError
from aiohttp_client_cache import CachedSession, CacheBackend

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
_SESSIONS_BY_EXPIRY = {}

def session(expiry=0):
    """Get a caching HTTP session"""

     # Testing requires caching be disabled or tests may fetch network data from previous tests which would be incorrect.
    if os.getenv("BLASEBALL_MIKE_NOCACHE", None):
        expiry = 0

    if expiry not in _SESSIONS_BY_EXPIRY:
        _SESSIONS_BY_EXPIRY[expiry] = CachedSession(cache=CacheBackend(expire_after=expiry))
    return _SESSIONS_BY_EXPIRY[expiry]


async def check_network_response(response):
    """Verify that network response is correct and is valid JSON"""
    response.raise_for_status()

    try:
        data = await response.json()
    except JSONDecodeError:
        raise ValueError("Network response is not valid JSON")

    return data
