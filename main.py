import json


class Book:
    def __init__(self):
        self.books = self.read_books_file()

    def __getitem__(self, key):
        return self.books[key]

    def estimate_reading_time(self, isbn, words_minute):
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

        return self

    def get_book_info(self, isbn):
        book_info = self.books[isbn]
        return book_info

    def read_books_file(self):
        with open("data/books.json") as file:
            books_json = json.load(file)
        return books_json


book = Book()
estimate_reading_time = book.estimate_reading_time("eISBN:978-0-553-90033-0", 250)
hours = str(estimate_reading_time.total_hours).split(".")[0]
minutes = str(estimate_reading_time.total_hours).split(".")[1]

print(
    "Estimated time for reading the book is %s hours and %s minutes." % (hours, minutes)
)  # 4 hours and 16 minutes for 250 words per minute.

print(
    book.get_book_info("eISBN:978-0-553-90033-0")
)  # simple return with the ISBN passed
