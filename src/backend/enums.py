from enum import StrEnum


class ReaderAction(StrEnum):
    READED = "readed"
    LISTENED = "listened"
    FAVOURITE = "favourite"
    WANTED = "wanted"
    BOUGHT = "bought"


class Genre(StrEnum):
    ROMANCE = "romance"
    DETECTIVE = "detective"
    NOIR = "noir"
    FANTASY = "fantasy"
    DRAMA = "drama"