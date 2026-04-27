from fastapi import Request

from . import deployment_router


@deployment_router.get()
async def healthcheck(request: Request):
    return 200
