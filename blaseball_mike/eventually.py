"""
Wrappers for eventually API for feed events

https://allie-signet.stoplight.io/docs/eventually/reference/eventually-api.v1.yaml
"""

from blaseball_mike.session import session, check_network_response

BASE_URL = 'https://api.sibr.dev/eventually'


async def search(cache_time=5, limit=100, query={}):
    """
    Search through feed events.
    Set to limit -1 to get everything.
    Returns a generator that only gets the following page when needed.
    Possible parameters for query: https://allie-signet.stoplight.io/docs/eventually/reference/eventually-api.v1.yaml/paths/~1events/get
    """
    s = session(cache_time)

    res_len = 0

    while limit == -1 or res_len < limit:
        out = await check_network_response(await s.get(f"{BASE_URL}/events",params={'offset': res_len, 'limit': 100, **query}))
        out_len = len(out)
        if out_len < 100:
            yield from out
            break
        else:
            res_len += out_len
            yield from out
