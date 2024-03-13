class Book:
    def __init__(self):
        self.title = "The Great Gatsby"
        self.author = "F. Scott Fitzgerald"
        self.pages = 218

    def estimate_reading_time(self, book_words_total, words_minute):
        self.total_minutes = book_words_total / words_minute

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


book = Book()
estimate_reading_time = book.estimate_reading_time(64_000, 250)
print(
    estimate_reading_time.total_hours
)  # 4 hours and 16 minutes for 250 words per minute.
