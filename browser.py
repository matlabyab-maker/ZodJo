import threading
import urllib.request
import urllib.parse

from html.parser import HTMLParser
from kivy.clock import Clock


class TextParser(HTMLParser):

    SKIP_TAGS = {
        "script",
        "style",
        "noscript",
        "svg"
    }

    BLOCK_TAGS = {
        "p", "div", "br", "h1", "h2",
        "h3", "li", "article", "section"
    }

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0:
            value = data.strip()

            if value:
                self.parts.append(value)

    def get_text(self):
        return "\n".join(self.parts)


class BrowserController:

    def __init__(self, app):
        self.app = app

    def normalize_url(self, value):
        value = value.strip()

        if not value:
            return ""

        # عبارت جست‌وجو
        if " " in value or "." not in value:
            query = urllib.parse.quote_plus(value)
            return "https://www.google.com/search?q=" + query

        if not value.startswith(("http://", "https://")):
            value = "https://" + value

        return value

    def open_url(self, url, callback):
        worker = threading.Thread(
            target=self._download,
            args=(url, callback),
            daemon=True
        )
        worker.start()

    def _download(self, url, callback):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Linux; Android 10) "
                        "AppleWebKit/537.36 "
                        "Chrome/120 Mobile Safari/537.36"
                    )
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=20
            ) as response:

                data = response.read(2_000_000)

                charset = (
                    response.headers.get_content_charset()
                    or "utf-8"
                )

            html = data.decode(
                charset,
                errors="replace"
            )

            parser = TextParser()
            parser.feed(html)

            text = parser.get_text().strip()

            if not text:
                text = "No readable text found."

            result = (url, text, None)

        except Exception as error:
            result = (
                url,
                "Unable to load page:\n" + str(error),
                error
            )

        # اجرای callback در نخ اصلی Kivy
        Clock.schedule_once(
            lambda dt: callback(*result),
            0
        )
