from fastapi import APIRouter

from .create_author import router as create_author_router
from .delete_author import router as delete_author_router
from .edit_author import router as edit_author_router

authors_router = APIRouter(prefix="/authors")
authors_router.include_router(create_author_router)
authors_router.include_router(delete_author_router)
authors_router.include_router(edit_author_router)
