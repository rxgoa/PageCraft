from typing import Optional
from fastapi import FastAPI
from app.models import BookModel
from app.services import Book

app = FastAPI()

book = Book()


#
# Fast API Methods
#
# Get all books available in data/books.json
# We can also filter by ISBN. /v1/api/books?isbn={{BOOK_ISBN}}
@app.get("/v1/api/books")
def get_books(isbn: Optional[str] = None):
    return book.get_book_info(isbn)


# Get Reading estimation from a Book
@app.get("/v1/api/books/estimation-reading")
def estimate_reading_time_wrapper(isbn: str, words_minute: int):
    return book.estimate_reading_time(isbn, words_minute)


# Get the most optimize place/chapter to stop reading given a time period.
@app.get("/v1/api/books/optimal-reading")
def optimize_time_read_wrapper(
    isbn: str, starting_point: int, time_to_read: int, words_minute: int
):
    optimize_time_formatted = book.optimize_time_read(
        isbn, starting_point, time_to_read, words_minute
    )

    return {"message": optimize_time_formatted, "status": 200}


# Insert new book into the JSON file
@app.post("/v1/api/books")
def insert_book(bookBody: BookModel):
    return book.create_new_book(bookBody)
