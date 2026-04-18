from os.path import join, exists
from os import remove as rm
from uuid import uuid4

from aiofiles import open
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.author import Author
from db.database import get_db
from schemas.audiobook import EditAudiobook

from . import authors_router


@authors_router.patch("/{author_id}")
async def patch_author(
    author_id: int,
    request: EditAudiobook,
    db: AsyncSession = Depends(get_db)
):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(404, f"Author with id {author_id} not found")
    
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)

    await db.commit()
    await db.refresh(author)
    return author