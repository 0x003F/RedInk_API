from fastapi import FastAPI, HTTPException
import os
import asyncio
import codecs
from tortoise import Tortoise, fields
from tortoise.models import Model
from models import *
from dotenv import load_dotenv

app=FastAPI()

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

@app.on_event("startup")
async def setup():
    await Tortoise.init(
    db_url=DB_URL,
    modules={'models':['models']}
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def close_orm():
    await Tortoise.close_connections()

def decode_escape_sequences(text: str)->str:
    try:
        return bytes(text, "utf-8").decode("unicode_escape")
    except Exception:
        return text



@app.get("/")
async def get_available_endpoints():
    endpoints=[
        {"method": "GET", "path": "/authors", "handler": "get_all_authors"},
        {"method": "GET", "path": "/authors/by-ID/{author_ID}", "handler": "author_from_ID"},
        {"method": "GET", "path": "/authors/by-name/{author_name}", "handler": "authors_by_name"},
        {"method": "GET", "path": "/authors/by-surname/{author_surname}", "handler": "authors_by_surname"},
        {"method": "GET", "path": "/books", "handler": "get_all_books"},
        {"method": "GET", "path": "/books/by-ID/{book_ID}", "handler": "get_books_by_ID"},
        {"method": "GET", "path": "/books/by-ID/{book_ID}/content", "handler": "get_book_content_by_ID"},
        {"method": "GET", "path": "/books/by-title/{book_title}", "handler": "get_books_by_title"},
        {"method": "GET", "path": "/books/by-author-name/{author_name}", "handler": "get_books_by_author_name"},
        {"method": "GET", "path": "/books/by-author-surname/{author_surname}", "handler": "get_books_by_author_surname"},
    ]
    return {
        "overview: ": "Available endpoints",
        "endpoints:": endpoints
    }


@app.get("/authors")
async def get_all_authors():
    authors_obj=await Author.all()
    JSONcontent=""

    if not authors_obj:
        raise HTTPException(status_code=404, detail="Authors not found")

    authors_list = []

    for author in authors_obj:
        authors_list.append({
            "author_ID": author.id,
            "author_name": author.name,
            "author_surname": author.surname
        })

    return {"authors": authors_list}

@app.get("/authors/by-ID/{author_ID}")
async def author_from_ID(author_ID: int):
    author_obj=await Author.filter(id=author_ID).first()

    if not author_obj:
        raise HTTPException(status_code=404, detail="Author not found")

    author_name=author_obj.name
    author_surname=author_obj.surname

    return {
        "author_ID": author_ID,
        "author_name": author_name,
        "author_surname": author_surname
    }

@app.get("/authors/by-name/{author_name}")
async def authors_by_name(author_name: str):
    authors_obj=await Author.filter(name__icontains=author_name)
    JSONcontent=""

    if not authors_obj:
        raise HTTPException(status_code=404, detail="Authors not found")

    authors_list=[]

    for author in authors_obj:
        authors_list.append({
            "author_ID": author.id,
            "author_name": author.name,
            "author_surname": author.surname
        })

    return {"authors": authors_list}

@app.get("/authors/by-surname/{author_surname}")
async def authors_by_surname(author_surname: str):
    authors_obj=await Author.filter(surname__icontains=author_surname)
    JSONcontent=""

    if not authors_obj:
        raise HTTPException(status_code=404, detail="Authors not found")

    authors_list=[]

    for author in authors_obj:
        authors_list.append({
            "author_ID": author.id,
            "author_name": author.name,
            "author_surname": author.surname
        })

    return {"authors": authors_list}

@app.get("/books")
async def get_all_books():
    books_obj=await Book.all().prefetch_related("authors")
    JSONcontent=""

    if not books_obj:
        raise HTTPException(status_code=404, detail="Books not found")

    books_list=[]
    authors_list=[]

    for book in books_obj:
        for author in book.authors:
            authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
            })

        books_list.append({
            "book_ID": book.id,
            "book_title": book.title,
            "authors": authors_list
        })
        authors_list=[]

    return {"books": books_list}

@app.get("/books/by-ID/{book_ID}")
async def get_books_by_ID(book_ID: int):
    books_obj=await Book.filter(id=book_ID).prefetch_related("authors")
    JSONcontent=""

    if not books_obj:
        raise HTTPException(status_code=404, detail="Book not found")

    books_list=[]

    for book in books_obj:
        authors_list=[]
        for author in book.authors:
            authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
            })

        books_list.append({
            "book_ID": book.id,
            "book_title": book.title,
            "authors": authors_list
        })

    return {"books": books_list}

@app.get("/books/by-ID/{book_ID}/content")
async def get_book_content_by_ID(book_ID: int):
    book_obj=await Book.get_or_none(id=book_ID).prefetch_related("authors")

    if not book_obj:
        raise HTTPException(status_code=404, detail="Book not found")

    book_info=[]
    authors_list=[]

    for author in book_obj.authors:
        authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
        })

    return {
        "book": {
            "book_ID": book_obj.id,
            "book_title": book_obj.title,
            "authors": authors_list,
            "content": decode_escape_sequences(book_obj.content)
        }
    }

@app.get("/books/by-title/{book_title}")
async def get_books_by_title(book_title: str):
    books_obj=await Book.filter(title__icontains=book_title).prefetch_related("authors")
    JSONcontent=""

    if not books_obj:
        raise HTTPException(status_code=404, detail="Books not found")

    books_list=[]

    for book in books_obj:
        authors_list=[]
        for author in book.authors:
            authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
            })

        books_list.append({
            "book_ID": book.id,
            "book_title": book.title,
            "authors": authors_list
        })

    return {"books": books_list}

@app.get("/books/by-author-name/{author_name}")
async def get_books_by_author_name(author_name: str):
    books_obj=await Book.filter(authors__name__icontains=author_name).prefetch_related("authors")
    JSONcontent=""

    if not books_obj:
        raise HTTPException(status_code=404, detail="Books not found")

    books_list=[]

    for book in books_obj:
        authors_list=[]
        for author in book.authors:
            authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
            })

        books_list.append({
            "book_ID": book.id,
            "book_title": book.title,
            "authors": authors_list
        })

    return {"books": books_list}

@app.get("/books/by-author-surname/{author_surname}")
async def get_books_by_author_surname(author_surname: str):
    books_obj=await Book.filter(authors__surname__icontains=author_surname).prefetch_related("authors")
    JSONcontent=""

    if not books_obj:
        raise HTTPException(status_code=404, detail="Books not found")

    books_list=[]

    for book in books_obj:
        authors_list=[]
        for author in book.authors:
            authors_list.append({
                "author_id": author.id,
                "author_name": author.name,
                "author_surname": author.surname
            })

        books_list.append({
            "book_ID": book.id,
            "book_title": book.title,
            "authors": authors_list
        })

    return {"books": books_list}