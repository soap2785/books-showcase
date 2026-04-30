from uuid import uuid4
from os.path import join

from aiofiles import open
from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from models.author import Author
from db.database import get_db
from schemas.book import AddBook

router = APIRouter()


@router.post("", response_model=dict)
async def add_book(request: AddBook, db: AsyncSession = Depends(get_db)):
    author = await db.get(Author, request.author)
    if not author:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Author with id {request.author} not found",
        )

    file_name = f"{uuid4()}.pdf"
    file_path = join("storage/books", file_name)
    async with open(file_path, "wb") as file:
        await file.write(request.file)

    new_book = Book(
        author_rel=author.id,
        title=request.title,
        description=request.description,
        genre=request.genre,
        pages=request.pages,
        is_mature_content=request.is_mature_content,
        file=file_path,
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return {"message": "Book added", "id": new_book.id}
