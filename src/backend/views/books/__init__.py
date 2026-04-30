from fastapi import APIRouter

from .add_book import router as add_book_router
from .delete_book import router as delete_book_router
from .edit_book import router as edit_book_router
from .get_books import router as get_books_router

books_router = APIRouter(prefix="/books")
books_router.include_router(add_book_router)
books_router.include_router(delete_book_router)
books_router.include_router(edit_book_router)
books_router.include_router(get_books_router)
