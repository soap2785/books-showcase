from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from models.author import Author
from db.database import get_db

router = APIRouter()


@router.get("/{author_id}", response_model=list)
async def get_books(author_id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(Author)
        .where(Author.id == author_id)
        .options(selectinload(Author.published_books))
    )
    result = await db.execute(query)
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )

    return author.published_books
