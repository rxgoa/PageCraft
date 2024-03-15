from typing import Optional
from fastapi import FastAPI
import json
import math

app = FastAPI()


class Book:
    def __init__(self):
        self.books = self.read_books_file()
        self.location_to_page = 13.035  # basically every 13.035 locations is considered a page compared to a printed book. Locations are used by Kindle to determine the location of the reader.
        self.words_per_page_aprox = 275  # this is a estimate for who many words there is a printed book. the number seems to be between 250 and 300.

    def __getitem__(self, key):
        return self.books[key]

    def estimate_reading_time(self, isbn: str, words_minute: int):
        book_info = self.get_book_info(isbn)
        self.total_minutes = book_info["word_count_aprox"] / words_minute
        prepare_time = str(format(self.total_minutes / 60, ".2f")).split(
            "."
        )  # split float number

        float_number_minutes = (
            int(prepare_time[1]) * 0.6
        )  # get value from float number (example: 0.8) and convert to minutes

        self.total_hours = (
            prepare_time[0] + "." + (str(float_number_minutes).split(".")[0])
        )

        hours = str(self.total_hours).split(".")[0]
        minutes = str(self.total_hours).split(".")[1]
        response_text = (
            "Estimated time for reading the book is %s hours and %s minutes."
            % (hours, minutes)
        )

        return {"message": response_text, "status": 200}

    def optimize_time_read(self, isbn, starting_point, time_to_read, words_minute):
        book_info = self.books[isbn]
        # we have to check if ISBN is from a e-book
        if book_info.get("is_ebook", False):
            print("[LOGGER] This is a e-book.")
            total_words_read = time_to_read * words_minute
            total_pages_read = total_words_read / self.words_per_page_aprox
            total_locations_read = total_pages_read * self.location_to_page
            last_chapter = {}

            for chapter in book_info.get("table_contents"):
                max_possible_locations_read = math.ceil(
                    starting_point + total_locations_read
                )

                if max_possible_locations_read > chapter["ebook"]["location_end"]:
                    last_chapter = chapter

            formatted_response = self.format_response(
                last_chapter, starting_point, time_to_read
            )

            return formatted_response
        else:
            print("[LOGGER] This isn't a e-book.")
            print(False)

    def format_response(self, chapter, starting_point, time_to_read):
        text_response = (
            "Given the time you have to read, which is %d minutes, and starting at location %d, I calculate that you can read up to location %d, the end of the chapter '%s'."
            % (
                time_to_read,
                starting_point,
                chapter["ebook"]["location_end"],
                chapter["title"],
            )
        )
        return text_response

    def get_book_info(self, isbn):
        if not isbn:
            book_info = self.books
            return book_info
        else:
            book_info = self.books[isbn]
            return book_info

    def read_books_file(self):
        with open("data/books.json") as file:
            books_json = json.load(file)
        return books_json


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
