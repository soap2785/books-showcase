from os.path import join, exists
from os import remove as rm

from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.audiobook import Audiobook

router = APIRouter()


@router.delete("/{audiobook_id}")
async def delete_audiobook(audiobook_id: int, db: AsyncSession = Depends(get_db)):
    audiobook = await db.get(Audiobook, audiobook_id)
    if not audiobook:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Audiobook with id {audiobook_id} not found"
        )

    file_path = join("storage/books", audiobook.file)

    try:
        await db.delete(audiobook)
        if exists(file_path):
            rm(file_path)

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(500, f"Ошибка при удалении: {str(e)}")

    return JSONResponse({}, status.HTTP_204_NO_CONTENT)
