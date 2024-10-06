# handler/converter.py

import html2text

class HtmlToMarkdownConverter:
    def __init__(self, html: str):
        self.html = html
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False

    def convert(self) -> str:
        return self.converter.handle(self.html)
