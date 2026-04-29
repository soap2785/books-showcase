from fastapi import APIRouter

from .add_audiobook import router as add_audiobook_router
from .delete_audiobook import router as delete_audiobook_router
from .edit_audiobook import router as edit_audiobook_router
from .get_audiobooks import router as get_audiobooks_router

audiobooks_router = APIRouter(prefix="/audiobooks")
audiobooks_router.include_router(add_audiobook_router)
audiobooks_router.include_router(delete_audiobook_router)
audiobooks_router.include_router(edit_audiobook_router)
audiobooks_router.include_router(get_audiobooks_router)
