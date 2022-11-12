from . import data
from bs4 import BeautifulSoup
from requests import Session
from .phase1 import load_book_page

def load_category_page(url: str | None, req_session: Session):
    books: list[data.BookData] = []
    if url is None:
        return (books, None)
    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        return (books, None)
    doc = BeautifulSoup(response.text, 'html.parser')
    section = doc.select_one('body>.page>.page_inner section')
    if section is None:
        return (books, None)
    articles = section.select('article.product_pod')
    for article in articles:
        links = article.select('a[href]:not([href=""])')
        if len(links) != 0:
            # TODO Check if it is an absolute value
            book = load_book_page(links[0].attrs["href"].strip(), req_session)
            if book is not None:
                books.append(book)
    # TODO Check if it is an absolute value
    next_page = section.select_one('ul.pager li.next a[href]:not([href=""])')
    return (books, next_page.attrs["href"].strip() if next_page is not None else None)

def load_category(url: str | None, req_session: Session):
    all_books: list[data.BookData] = []
    while (res := load_category_page(url, req_session)) is not None:
        books, url = res
        all_books.extend(books)
    return all_books

if __name__ == "__main__":
    pass
