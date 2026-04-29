from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.author import Author
from models.user import User
from db.database import get_db
from schemas.author import CreateAuthor

router = APIRouter()


@router.post("/{user_id}", response_model=dict)
async def create_author(
    user_id: int, request: CreateAuthor, db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"User with id {user_id} not found",
        )

    if user.type == "author":
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"User with id {user_id} is already an author",
        )

    user.type = "author"
    new_author = Author(
        id=user_id,
        fullname=request.fullname,
        description=request.description,
    )
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return {"message": "Author created", "id": new_author.id}
