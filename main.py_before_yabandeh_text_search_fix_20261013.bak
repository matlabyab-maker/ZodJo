from pathlib import Path
from urllib.parse import urlparse
import threading
import webbrowser

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.core.text import LabelBase
from kivy.uix.scrollview import ScrollView
from html import unescape


def _yabandeh_persian_text(value):
    """آماده‌سازی متن فارسی برای نمایش در Kivy."""
    value = str(value)
    if not any("\u0600" <= char <= "\u06ff" for char in value):
        return value
    try:
        return get_display(arabic_reshaper.reshape(value), base_dir="R")
    except Exception:
        return value

BASE = Path("/storage/emulated/0/Yabandeh")
(BASE / "data").mkdir(parents=True, exist_ok=True)
(BASE / "downloads").mkdir(parents=True, exist_ok=True)
(BASE / "pages").mkdir(parents=True, exist_ok=True)

# بارگذاری ماژول‌ها با حفظ سازگاری با هر دو ساختار
try:
    from core.history import HistoryManager
except ImportError:
    HistoryManager = None

try:
    from core.bookmarks import BookmarkManager
except ImportError:
    BookmarkManager = None

try:
    from core.settings import SettingsManager
except ImportError:
    SettingsManager = None

try:
    from core.search_engine import SearchEngine
except ImportError:
    SearchEngine = None

try:
    from core.page_saver import save_page
except ImportError:
    save_page = None



# اصلاح متن فارسی دکمه‌ها
def Button(*args, **kwargs):
    if "text" in kwargs and isinstance(kwargs["text"], str):
        kwargs["text"] = _yabandeh_persian_text(
            kwargs["text"]
        )
    elif args and isinstance(args[0], str):
        args = (
            _yabandeh_persian_text(args[0]),
        ) + args[1:]

    return KivyButton(*args, **kwargs)


class YabandehApp(App):
    def build(self):
        font_path = Path("/storage/emulated/0/Yabandeh/fonts/NotoNaskhArabic.ttf")
        LabelBase.register(name="YabandehArabic", fn_regular=str(font_path))
        self.title = "Yabandeh"
        self.history = HistoryManager() if HistoryManager else None
        self.bookmarks = BookmarkManager() if BookmarkManager else None
        self.settings = SettingsManager() if SettingsManager else None
        self.search = SearchEngine() if SearchEngine else None

        self.current_url = ""
        self.current_title = "Yabandeh"
        self.current_text = ""
        self.back_stack = []

        root = BoxLayout(orientation="vertical", spacing=3, padding=4)

        address_row = BoxLayout(size_hint_y=None, height=44, spacing=3)
        self.address = TextInput(
            font_name="YabandehArabic",
            hint_text=_yabandeh_persian_text("آدرس سایت یا عبارت جست‌وجو"),
            multiline=False,
            halign="right",
            size_hint_x=1
        )
        # متن خام جست‌وجو حفظ می‌شود؛ شکل‌دهی فقط هنگام از دست رفتن فوکوس
        # انجام می‌شود تا متن ارسالی به موتور جست‌وجو خراب نشود.
        self._address_raw = ""
        self._address_rendering = False
        self.address.bind(text=self._address_text_changed)
        self.address.bind(focus=self._address_focus_changed)
        self.address.bind(on_text_validate=lambda *_: self.open_address())
        address_row.add_widget(self.address)
        address_row.add_widget(
            Button(text="برو", font_name="YabandehArabic", size_hint_x=None, width=58,
                   on_release=lambda *_: self.open_address())
        )
        root.add_widget(address_row)

        toolbar = BoxLayout(size_hint_y=None, height=42, spacing=2)
        for title, action in [
            ("خانه", self.home),
            ("نشانک", self.add_bookmark),
            ("تاریخچه", self.show_history),
            ("ذخیره", self.save_current_page),
            ("دانلود", self.download_current),
        ]:
            toolbar.add_widget(
                Button(text=title, font_name="YabandehArabic", on_release=lambda _, fn=action: fn())
            )
        root.add_widget(toolbar)

        self.status = Label(
            font_name="YabandehArabic",
            text="آماده",
            size_hint_y=None,
            height=28
        )
        root.add_widget(self.status)

        self.page = Label(
            font_name="YabandehArabic",
            text="Yabandeh آماده است.\nآدرس سایت را وارد کن.",
            size_hint_y=None,
            halign="right",
            valign="top"
        )
        self.page.bind(
            width=lambda instance, value:
            setattr(instance, "text_size", (value, None)),
            texture_size=lambda instance, value:
            setattr(instance, "height", value[1])
        )

        scroll = ScrollView()
        scroll.add_widget(self.page)
        root.add_widget(scroll)

        bottom = BoxLayout(size_hint_y=None, height=38, spacing=2)
        bottom.add_widget(
            Button(text="بازگشت", font_name="YabandehArabic", on_release=lambda *_: self.go_back())
        )
        bottom.add_widget(
            Button(text="پاک‌کردن", font_name="YabandehArabic", on_release=lambda *_: self.clear_page())
        )
        bottom.add_widget(
            Button(text="خروج", font_name="YabandehArabic", on_release=lambda *_: self.stop())
        )
        root.add_widget(bottom)

        return root

    def set_status(self, message):
        self.status.text = _yabandeh_persian_text(message)

    def open_address(self):
        text = (self._address_raw if self.address.focus else self._address_raw or self.address.text).strip()
        if not text:
            self.set_status("آدرس یا عبارت جست‌وجو را وارد کن.")
            return

        if self.search:
            url = self.search.resolve(text)
        else:
            parsed = urlparse(text)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                url = text
            elif " " not in text and "." in text:
                url = "https://" + text
            else:
                from urllib.parse import quote
                url = "https://www.google.com/search?q=" + quote(text)

        self.load_page(url)

    def load_page(self, url, add_to_back=True):
        if add_to_back and self.current_url and self.current_text:
            if self.current_url != url:
                self.back_stack.append({
                    "url": self.current_url,
                    "title": self.current_title,
                    "text": self.current_text,
                })

                # محدود کردن حافظهٔ تاریخچهٔ بازگشت
                self.back_stack = self.back_stack[-50:]

        self.current_url = url
        self._address_raw = url
        self._address_rendering = True
        self.address.text = url
        self._address_rendering = False
        self.set_status("در حال دریافت صفحه...")

        threading.Thread(
            target=self._fetch_page,
            args=(url,),
            daemon=True
        ).start()

    def _address_text_changed(self, instance, value):
        if not self._address_rendering and instance.focus:
            self._address_raw = value

    def _address_focus_changed(self, instance, focused):
        self._address_rendering = True
        try:
            if focused:
                # هنگام ویرایش، متن بدون شکل‌دهی باشد تا ویرایش و جست‌وجو سالم بماند.
                instance.text = self._address_raw
            else:
                self._address_raw = instance.text
                instance.text = _yabandeh_persian_text(self._address_raw)
        finally:
            self._address_rendering = False

    def _fetch_page(self, url):
        try:
            import urllib.request
            from html.parser import HTMLParser
            from email.message import Message

            class TextExtractor(HTMLParser):
                BLOCK_TAGS = {
                    "address", "article", "aside", "blockquote", "br", "dd",
                    "div", "dl", "dt", "fieldset", "figcaption", "figure",
                    "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
                    "header", "hr", "li", "main", "nav", "ol", "p", "pre",
                    "section", "table", "tr", "ul"
                }
                SKIP_TAGS = {"script", "style", "noscript", "svg", "iframe"}

                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.parts = []
                    self.title_parts = []
                    self.in_title = False
                    self.skip_depth = 0

                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag in self.SKIP_TAGS:
                        self.skip_depth += 1
                        return
                    if self.skip_depth:
                        return
                    if tag == "title":
                        self.in_title = True
                    if tag in self.BLOCK_TAGS:
                        self.parts.append("\n")
                    if tag == "img":
                        alt = (attrs.get("alt") or "").strip()
                        if alt:
                            self.parts.append(" [تصویر: " + alt + "] ")

                def handle_startendtag(self, tag, attrs):
                    self.handle_starttag(tag, attrs)
                    self.handle_endtag(tag)

                def handle_endtag(self, tag):
                    if tag in self.SKIP_TAGS and self.skip_depth:
                        self.skip_depth -= 1
                        return
                    if self.skip_depth:
                        return
                    if tag == "title":
                        self.in_title = False
                    if tag in self.BLOCK_TAGS:
                        self.parts.append("\n")

                def handle_data(self, data):
                    if self.skip_depth:
                        return
                    value = " ".join(data.split())
                    if not value:
                        return
                    if self.in_title:
                        self.title_parts.append(value)
                    # متن‌های خام بین تگ‌ها را با فاصله/خط جدا می‌کنیم.
                    self.parts.append(value + " ")

                def result(self):
                    text = "".join(self.parts)
                    lines = [" ".join(line.split()) for line in text.splitlines()]
                    text = "\n".join(line for line in lines if line)
                    return "\n".join(self.title_parts).strip(), text.strip()

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 "
                        "Chrome/120 Mobile Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.7",
                },
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read(4 * 1024 * 1024)
                charset = response.headers.get_content_charset()
                final_url = response.geturl()

            # اگر سرور charset نداده باشد، ابتدا UTF-8 و سپس fallback را امتحان می‌کنیم.
            try:
                html = raw.decode(charset or "utf-8", errors="replace")
            except LookupError:
                html = raw.decode("utf-8", errors="replace")

            parser = TextExtractor()
            parser.feed(html)
            title, text = parser.result()
            if not text:
                text = (
                    "متن قابل استخراج از این صفحه پیدا نشد.\n"
                    "ممکن است سایت با JavaScript ساخته شده باشد یا دسترسی را محدود کرده باشد.\n"
                    "این نسخه محتوای متنی HTML را استخراج می‌کند و هنوز موتور نمایش کامل صفحات وب نیست."
                )
            Clock.schedule_once(
                lambda dt: self._page_loaded(final_url, text, title), 0
            )

        except Exception as exc:
            Clock.schedule_once(
                lambda dt, error=str(exc): self._page_error(error), 0
            )

    def _page_loaded(self, url, text, title=""):
        self.current_url = url
        self.current_text = text
        self.current_title = title or url
        self.page.text = _yabandeh_persian_text(text)
        self.set_status("متن صفحه دریافت شد؛ تصاویر و صفحات JavaScript هنوز پشتیبانی کامل ندارند.")

        if self.history:
            try:
                self.history.add(url, url)
            except Exception as exc:
                self.set_status("صفحه باز شد؛ ثبت تاریخچه ناموفق بود.")

    def _page_error(self, message):
        self.page.text = _yabandeh_persian_text("بازکردن صفحه ناموفق بود.\n" + message)
        self.set_status("خطا در دریافت صفحه")

    def home(self):
        self.address.text = "https://www.google.com"
        self.load_page(self.address.text)

    def add_bookmark(self):
        if not self.current_url:
            self.set_status("ابتدا یک صفحه باز کن.")
            return
        if not self.bookmarks:
            self.set_status("ماژول نشانک در دسترس نیست.")
            return
        try:
            added = self.bookmarks.add(self.current_url, self.current_title)
            self.set_status("نشانک ثبت شد." if added else "نشانک به‌روز شد.")
        except Exception as exc:
            self.set_status("خطا در ثبت نشانک: " + str(exc))

    def show_history(self):
        if not self.history:
            self.set_status("ماژول تاریخچه در دسترس نیست.")
            return
        try:
            items = self.history.get_all()
            self.page.text = _yabandeh_persian_text("\n\n".join(
                str(item.get("title", "")) + "\n" +
                str(item.get("url", ""))
                for item in items[:100]
            ) or "تاریخچه خالی است.")
            self.set_status("تاریخچه")
        except Exception as exc:
            self.set_status("خطا در تاریخچه: " + str(exc))

    def save_current_page(self):
        if not self.current_text:
            self.set_status("صفحه‌ای برای ذخیره وجود ندارد.")
            return

        try:
            if save_page:
                path = save_page(
                    self.current_text,
                    self.current_title,
                    extension="txt"
                )
            else:
                from datetime import datetime

                folder = BASE / "pages"
                folder.mkdir(parents=True, exist_ok=True)

                path = folder / (
                    "page_" +
                    datetime.now().strftime("%Y%m%d_%H%M%S") +
                    ".txt"
                )
                path.write_text(
                    self.current_text,
                    encoding="utf-8"
                )

            self.set_status("ذخیره شد: " + str(path))

        except Exception as exc:
            self.set_status("خطا در ذخیره: " + str(exc))

    def download_current(self):
        if not self.current_url:
            self.set_status("ابتدا یک صفحه باز کن.")
            return

        try:
            from core.downloads import DownloadManager

            manager = DownloadManager()
            self.set_status("دانلود شروع شد...")

            manager.download(
                self.current_url,
                callback=self._download_callback
            )

        except Exception as exc:
            self.set_status("خطای شروع دانلود: " + str(exc))

    def _download_callback(self, success, message, path):
        if success:
            status = "دانلود انجام شد: " + str(message)
        else:
            status = "خطای دانلود: " + str(message)

        Clock.schedule_once(
            lambda dt, msg=status: self.set_status(msg),
            0
        )

    def go_back(self):
        if not self.back_stack:
            self.set_status("صفحهٔ قبلی در دسترس نیست.")
            return

        previous = self.back_stack.pop()

        self.current_url = previous["url"]
        self.current_title = previous["title"]
        self.current_text = previous["text"]

        self._address_raw = self.current_url
        self._address_rendering = True
        self.address.text = self.current_url
        self._address_rendering = False
        self.page.text = _yabandeh_persian_text(self.current_text)
        self.set_status("به صفحهٔ قبلی برگشتی.")

    def clear_page(self):
        self.page.text = ""
        self.current_text = ""
        self.set_status("محتوای نمایشی پاک شد.")


if __name__ == "__main__":
    YabandehApp().run()
