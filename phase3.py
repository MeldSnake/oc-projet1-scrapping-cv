
from typing import TypedDict
from urllib.parse import ParseResult

from bs4 import BeautifulSoup
from requests import Session

import data
from phase2 import load_category


def load_all_categories():
    with Session() as req_session:
        response = req_session.get(data.BOOK_TO_SCRAPE_ROOT_URL)
        if not response.ok or response.status_code != 200:
            categories = []
        else:
            doc = BeautifulSoup(response.content, 'html.parser')
            categories = doc.select('.page .side_categories>ul>li>ul>li>a')
    for category in categories:
        if (href := category.attrs.get('href', '').strip()) != '':
            category_name = category.text.strip()
            category_url = data.get_full_url(href, data.BOOK_TO_SCRAPE_ROOT_URL)
            books = load_category(category_url, req_session)
            data.write_csv('./%s.csv' % (category_name), books)


if __name__ == "__main__":
    books = load_all_categories()
