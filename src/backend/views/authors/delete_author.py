from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from models.author import Author
from db.database import get_db

router = APIRouter()


@router.delete("/{author_id}", response_model=dict)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Author with id {author_id} not found"
        )

    await db.delete(author)
    await db.commit()
    return JSONResponse({}, status.HTTP_204_NO_CONTENT)
