from pydantic import BaseModel
from typing import List

class AuthorCreate(BaseModel):
    name: str
    surname: str

class BookCreate(BaseModel):
    title: str
    content: str
    author_id: List[int]
