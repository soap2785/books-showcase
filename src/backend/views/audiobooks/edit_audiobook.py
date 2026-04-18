from os.path import join, exists
from os import remove as rm
from uuid import uuid4

from aiofiles import open
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.audiobook import Audiobook
from db.database import get_db
from schemas.audiobook import EditAudiobook

from . import audiobooks_router


@audiobooks_router.patch("/{audiobook_id}")
async def patch_audiobook(
    audiobook_id: int, request: EditAudiobook, db: AsyncSession = Depends(get_db)
):
    audiobook = await db.get(Audiobook, audiobook_id)
    if not audiobook:
        raise HTTPException(404, f"Audiobook with id {audiobook_id} not found")

    update_data = request.model_dump(exclude_unset=True)
    if "file" in update_data:
        new_file_name = f"{uuid4()}.mp3"
        new_path = join("storage/audiobooks", new_file_name)
        async with open(new_path, "wb") as f:
            await f.write(update_data["file"])

        if audiobook.file and exists(audiobook.file):
            rm(audiobook.file)

        update_data["file"] = new_path

    for key, value in update_data.items():
        setattr(audiobook, key, value)

    await db.commit()
    await db.refresh(audiobook)
    return audiobook
