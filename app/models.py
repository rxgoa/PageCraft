from typing import List, Optional
from pydantic import BaseModel


class EbookModel(BaseModel):
    location_start: int
    location_end: int


class PrintedBookModel(BaseModel):
    page_start: int
    page_end: int


class BookTableContentModel(BaseModel):
    title: str
    order: int
    ebook: Optional[EbookModel]
    printed: Optional[PrintedBookModel]


class BookModel(BaseModel):
    title: str
    author: str
    isbn: str
    total_pages: int
    total_locations: int
    is_ebook: bool
    word_count_aprox: int
    location_to_page: float
    table_contents: List[BookTableContentModel]
