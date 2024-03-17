import os
from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.models import BookModel
from app.services import Book

# FastAPI config
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory="app/templates")

book = Book()


#
#
# Server Rendering Views (HTML)
#
#
@app.get("/find-book", response_class=HTMLResponse)
async def find_book(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("book.html", context)


@app.get("/how-long-to-read", response_class=HTMLResponse)
async def how_long_to_read(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("how_long_read.html", context)


@app.get("/optimal-read", response_class=HTMLResponse)
async def optimal_read(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("optimal_read.html", context)


#
# Fast API Methods
#
# Get all books available in data/books.json
# We can also filter by ISBN. /v1/api/books?isbn={{BOOK_ISBN}}
@app.get("/v1/api/books")
def get_books(
    request: Request,
    isbn: Optional[str] = None,
    hx_request: Optional[str] = Header(None),
):
    if hx_request:
        book_requested = book.get_book_info(isbn)
        context = {"request": request, "book": book_requested}
        return templates.TemplateResponse("book_info.html", context)
    else:
        return book.get_book_info(isbn)


# Get Reading estimation from a Book
@app.get("/v1/api/books/estimation-reading")
def estimate_reading_time_wrapper(
    request: Request,
    isbn: str,
    words_minute: int,
    hx_request: Optional[str] = Header(None),
):
    if hx_request:
        book_estimate_reading_time = book.estimate_reading_time(isbn, words_minute)
        context = {"request": request, "book": book_estimate_reading_time}
        return templates.TemplateResponse("how_long_read_info.html", context)
    else:
        return book.estimate_reading_time(isbn, words_minute)


# Get the most optimize place/chapter to stop reading given a time period.
@app.get("/v1/api/books/optimal-reading")
def optimize_time_read_wrapper(
    request: Request,
    isbn: str,
    starting_point: int,
    time_to_read: int,
    words_minute: int,
    hx_request: Optional[str] = Header(None),
):
    optimize_time_formatted = book.optimize_time_read(
        isbn, starting_point, time_to_read, words_minute
    )
    if hx_request:
        book_response = {"message": optimize_time_formatted}
        context = {"request": request, "book": book_response}
        return templates.TemplateResponse("optimal_read_info.html", context)
    else:
        return {"message": optimize_time_formatted, "status": 200}


# Insert new book into the JSON file
@app.post("/v1/api/books")
def insert_book(bookBody: BookModel):
    return book.create_new_book(bookBody)
