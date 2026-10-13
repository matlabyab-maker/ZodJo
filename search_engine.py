from urllib.parse import quote, urlparse


class SearchEngine:
    def __init__(self):
        self.engines = {
            "Google": "https://www.google.com/search?q=",
            "Bing": "https://www.bing.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Yahoo": "https://search.yahoo.com/search?p=",
            "Brave": "https://search.brave.com/search?q=",
            "Startpage": "https://www.startpage.com/sp/search?query="
        }
        self.active = "Google"

    def set_engine(self, name):
        if name not in self.engines:
            raise ValueError("موتور جست‌وجو شناخته نشد")
        self.active = name

    def get_engines(self):
        return list(self.engines.keys())

    def search_url(self, query):
        query = str(query).strip()
        if not query:
            return ""
        return self.engines[self.active] + quote(query)

    def resolve(self, text):
        text = str(text).strip()
        if not text:
            return ""

        parsed = urlparse(text)

        if parsed.scheme in ("http", "https") and parsed.netloc:
            return text

        if " " not in text and "." in text:
            candidate = "https://" + text
            parsed = urlparse(candidate)
            if parsed.netloc and "." in parsed.netloc:
                return candidate

        return self.search_url(text)
