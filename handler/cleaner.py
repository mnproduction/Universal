# handler/cleaner.py

import re
from bs4 import BeautifulSoup

class HtmlCleaner:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def clean_html(self) -> str:
        for element in self.soup.find_all('header', 'footer', 'nav', 'aside'):
            element.decompose()
        return str(self.soup)

class UrlRemover:
    def __init__(self, markdown: str):
        self.markdown = markdown

    def remove_urls(self) -> str:
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        return re.sub(url_pattern, "", self.markdown)


