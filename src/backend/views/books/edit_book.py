from os.path import join, exists
from os import remove as rm
from uuid import uuid4

from aiofiles import open
from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from db.database import get_db
from schemas.book import EditBook

router = APIRouter()


@router.patch("/{book_id}")
async def patch_book(
    book_id: int, request: EditBook, db: AsyncSession = Depends(get_db)
):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(404, f"Book with id {book_id} not found")

    update_data = request.model_dump(exclude_unset=True)
    if "file" in update_data:
        new_file_name = f"{uuid4()}.pdf"
        new_path = join("storage/books", new_file_name)
        async with open(new_path, "wb") as f:
            await f.write(update_data["file"])

        if book.file and exists(book.file):
            rm(book.file)

        update_data["file"] = new_path

    for key, value in update_data.items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)
    return book
