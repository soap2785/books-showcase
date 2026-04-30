from os.path import join, exists
from os import remove as rm

from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.book import Book

router = APIRouter()


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Book with id {book_id} not found"
        )

    file_path = join("storage/books", book.file)

    try:
        await db.delete(book)
        if exists(file_path):
            rm(file_path)

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(500, f"Ошибка при удалении: {str(e)}")

    return JSONResponse({}, status.HTTP_204_NO_CONTENT)
