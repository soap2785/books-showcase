from os.path import join
from uuid import uuid4

from aiofiles import open
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.audiobook import Audiobook
from models.author import Author
from db.database import get_db
from schemas.audiobook import AddAudiobook

from . import audiobooks_router


@audiobooks_router.post("", response_model=dict)
async def add_audiobook(request: AddAudiobook, db: AsyncSession = Depends(get_db)):
    author = await db.get(Author, request.author)
    if not author:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Author with id {request.author} not found",
        )

    file_name = f"{uuid4()}.mp3"
    file_path = join("storage/audiobooks", file_name)
    async with open(file_path, "wb") as f:
        await f.write(request.file)

    new_audiobook = Audiobook(
        author_rel=author.id,
        title=request.title,
        description=request.description,
        genre=request.genre,
        is_mature_content=request.is_mature_content,
        file=file_path,
    )
    db.add(new_audiobook)
    await db.commit()
    await db.refresh(new_audiobook)
    return {"message": "Audiobook added", "id": new_audiobook.id}