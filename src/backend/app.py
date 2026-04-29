from fastapi import FastAPI

from views.audiobooks import audiobooks_router
from views.authors import authors_router
from views.books import books_router
from views.deployment import deployment_router

app = FastAPI()
app.include_router(deployment_router)
app.include_router(audiobooks_router)
app.include_router(authors_router)
app.include_router(books_router)
