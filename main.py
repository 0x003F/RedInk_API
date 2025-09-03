from fastapi import FastAPI
import os
import asyncio
from tortoise import Tortoise, fields
from tortoise.models import Model
from models import Author, Book
from dotenv import load_dotenv


app=FastAPI()

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

async def setup():
    await Tortoise.init(
    db_url=DB_URL,
    modules={'models':['models']}
    )
    await Tortoise.generate_schemas()


@app.get("/")
async def root():
    return {"greeting":"Hello world"}
