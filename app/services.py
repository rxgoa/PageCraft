import json
import math
from app.models import BookModel

path_json = "data/books.json"


class Book:
    def __init__(self):
        self.books = self.read_books_file()
        self.location_to_page = 13.035  # basically every 13.035 locations is considered a page compared to a printed book. Locations are used by Kindle to determine the location of the reader.
        self.words_per_page_aprox = 275  # this is a estimate for who many words there is a printed book. the number seems to be between 250 and 300.

    def __getitem__(self, key):
        return self.books[key]

    def create_new_book(self, bookBody: BookModel):
        books = self.get_book_info(None)
        current_book_isbn = bookBody.isbn
        check_existence = books.get(current_book_isbn)
        if check_existence is None or check_existence == "":
            books[current_book_isbn] = bookBody.model_dump()
            self.insert_book(books)
            return {"message": "Book inserted!", "data": bookBody}
        else:
            return {"message": "Book already exists in JSON file."}

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

    def insert_book(self, book):
        with open(path_json, "w") as file:
            json.dump(book, file, indent=4)
            return

    def get_book_info(self, isbn):
        if isbn is None or isbn == "":
            book_info = self.books
            return book_info
        else:
            book_info = self.books[isbn.lower()]
            return book_info

    def read_books_file(self):
        with open(path_json) as file:
            books_json = json.load(file)
        return books_json
