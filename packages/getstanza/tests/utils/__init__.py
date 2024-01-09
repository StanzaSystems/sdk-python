import asyncio


def noop(*args, **kwargs):
    return None


async def async_noop(*args, **kwargs):
    return None


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
