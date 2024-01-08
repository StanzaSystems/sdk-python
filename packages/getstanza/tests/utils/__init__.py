def noop(*args, **kwargs):
    return None


async def async_noop(*args, **kwargs):
    return None


async def async_return(result):
    return result
