from fastapi import Request, APIRouter

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(request: Request):
    return 200
