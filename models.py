from tortoise import fields
from tortoise.models import Model

class Author(Model):
    id=fields.IntField(pk=True) #auto-increment by default
    name=fields.CharField(max_length=32)
    surname = fields.CharField(max_length=64)

class Book(Model):
    id=fields.IntField(pk=True) #auto-increment by default
    title=fields.CharField(max_length=255)
    content=fields.TextField() #whole book's text

    #N-N relationship between Author and Book
    authors=fields.ManyToManyField("models.Author", related_name="books")
