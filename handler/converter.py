# handler/converter.py

import html2text

class HtmlToMarkdownConverter:
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False

    def convert(self, html: str) -> str:
        return self.converter.handle(html)
