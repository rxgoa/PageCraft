# PageCraft
The "PageCraft - MinMaxing your reading" project is an web application designed to help users estimate the time required to finish a book based on their reading speed. Users input the book they want to read and their words-per-minute reading pace, receiving an estimate of the total reading hours.

### **Features:**

1. **Time Estimation:**
    
    - Users input the book title and reading speed to get an estimate of how many hours it would take to complete the entire book.
2. **Optimal Stop Point:**
    
    - An additional feature allows users to specify the time they have available for reading. Given the current page or chapter, the system suggests where to stop to avoid losing track of the plot the next day.


### Books Dataset
Well, this this code needs the table of contents for each book, so it can now where a chapter starts and ends. Without this information, we cannot calculate the best chapter point to stop reading (feature). So, for now at least, the book dataset is being done by me and I'm storing the information in `data/books.json`. Since this project is just for me to use I don't mind typing the books I'm reading (it's table of contents). Maybe this one day will help somebody.

## Running this Application
For you to run this api you will need `python3` installed. After you need to run `pip install -r requirements.txt`. This will install `fastapi` and `typing` packages. You could also create a `virtual envirment` with Python `python3 -m venv env` and then `source env/bin/activate`. For running our web server, we're going to need `Uvicorn` for this. Just install using `pip install "uvicorn[standart]".

Then, you can run `uvicorn main:app --reload`.

### API
For now, the API has only 2 endpoints: 

- `[GET] http://localhost:8000/v1/api/books/estimation-reading` This endpoint will tell you how long (in hours and minutes) it would take for you to read a given book.
    - `isbn`: ISBN code for the Book. See `data/books.json` for more info.
    - `words_minute`: How many words can you read in a minute. For this info, you could try this website http://www.freereadingtest.com/
- `[GET] http://localhost:8000/v1/api/books/optimal-reading` This endpoint will tell you the best chapter to stop reading given a time frame you have to read. This endpoint will tell the last chapter in a given book where you can stop and not get lost tomorrow when continued reading.
    - `isbn`: ISBN code for the Book. See `data/books.json` for more info.
    - `starting_point`: This is the Page number or Location point you're stating your reading Session. The `location point` is used by Kindle to track your progress.
    - `time_to_read`: How much time do you have to read. Time is in minutes.
    - `words_minute`: How many words can you read in a minute. For this info, you could try this website http://www.freereadingtest.com/
