import csv
import data
from bs4 import BeautifulSoup
from requests import Session
from phase1 import load_book_page
from urllib.parse import ParseResult, urljoin, urlparse


def load_category_page(url: str | None, req_session: Session):
    books: list[data.BookData] = []
    url = data.get_full_url(url, None)
    if url is None:
        return None

    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        return None
    doc = BeautifulSoup(response.text, 'html.parser')

    section = doc.select_one('body>.page>.page_inner section')
    if section is None:
        return None

    articles = section.select('article.product_pod')
    for article in articles:
        links = article.select('a[href]:not([href=""])')
        if len(links) != 0:
            book = load_book_page(
                data.get_full_url(links[0].attrs["href"].strip(), url),
                req_session
            )
            if book is not None:
                books.append(book)

    next_page = section.select_one('ul.pager li.next a[href]:not([href=""])')
    if next_page is not None:
        next_page_url = data.get_full_url(next_page.attrs['href'].strip(), url)
    else:
        next_page_url = None
    return (books, next_page_url)


def load_category(url: str | None, req_session: Session):
    all_books: list[data.BookData] = []
    while (res := load_category_page(url, req_session)) is not None:
        books, url = res
        all_books.extend(books)
    return all_books


if __name__ == "__main__":
    import sys
    session = Session()
    if len(sys.argv) > 1:
        books = load_category(sys.argv[1], session)
        data.write_csv("./phase2.csv", books)
