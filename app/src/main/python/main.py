# -*- coding: utf-8 -*-
"""
ZodJo Python entry point.
This is a lightweight Kivy prototype shell.
"""

from pathlib import Path
import json
import webbrowser

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

ROOT = Path(__file__).resolve().parents[4]
ASSET_DIR = ROOT / "app" / "src" / "main" / "assets"
STATE_DIR = Path.home() / ".zodjo"
STATE_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = STATE_DIR / "history.json"
BOOKMARK_FILE = STATE_DIR / "bookmarks.json"


def read_list(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def write_list(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


class ZodJoApp(App):
    def build(self):
        self.title = "ZodJo"
        self.phone_mode = False
        self.zoom_level = 100
        self.history = read_list(HISTORY_FILE)
        self.bookmarks = read_list(BOOKMARK_FILE)

        root = BoxLayout(orientation="vertical", spacing=2, padding=2)

        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="34dp",
            spacing=2
        )

        buttons = [
            ("Send", self.send_action),
            ("File", self.file_action),
            ("Copy MW", self.copy_page_action),
            ("Paste", self.paste_action),
            ("Translate", self.translate_action),
            ("Muse", self.muse_action),
            ("PC/Phone", self.toggle_device),
            ("Setup", self.setup_action),
        ]

        for title, callback in buttons:
            button = Button(
                text=title,
                font_size="10sp",
                size_hint_x=None,
                width="66dp"
            )
            button.bind(on_release=callback)
            top.add_widget(button)

        root.add_widget(top)

        address_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="42dp",
            spacing=3
        )

        self.address = TextInput(
            hint_text="Address or search",
            multiline=False,
            font_size="13sp"
        )
        self.address.bind(on_text_validate=self.navigate)

        go_button = Button(text="Go", size_hint_x=None, width="52dp")
        go_button.bind(on_release=self.navigate)

        address_row.add_widget(self.address)
        address_row.add_widget(go_button)
        root.add_widget(address_row)

        self.page_label = Label(
            text="ZodJo\nEnter an address or search term above.",
            halign="center",
            valign="middle"
        )
        self.page_label.bind(size=self.page_label.setter("text_size"))
        root.add_widget(self.page_label)

        bottom = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="32dp",
            spacing=2
        )

        bottom_buttons = [
            ("History", self.show_history),
            ("Bookmarks", self.show_bookmarks),
            ("Clean", self.clear_history),
            ("Save Page", self.save_page),
            ("Copy", self.copy_address),
            ("Text Size", self.change_text_size),
        ]

        for title, callback in bottom_buttons:
            button = Button(text=title, font_size="10sp")
            button.bind(on_release=callback)
            bottom.add_widget(button)

        root.add_widget(bottom)

        self.status = Label(
            text="ZodJo ready",
            size_hint_y=None,
            height="18dp",
            font_size="10sp"
        )
        root.add_widget(self.status)

        self._hour_key = None
        Clock.schedule_interval(self.hourly_effect, 0.5)

        return root

    def notify(self, message):
        self.status.text = message
        Clock.unschedule(self.reset_status)
        Clock.schedule_once(self.reset_status, 4)

    def reset_status(self, _dt):
        self.status.text = "ZodJo ready"

    def navigate(self, *_args):
        value = self.address.text.strip()
        if not value:
            return

        if "://" not in value:
            if "." in value and " " not in value:
                value = "https://" + value
            else:
                value = "https://www.google.com/search?q=" + value.replace(
                    " ", "+"
                )

        self.address.text = value
        self.history.insert(0, value)
        self.history = self.history[:100]
        write_list(HISTORY_FILE, self.history)

        # Opens the destination using the system's available browser.
        # This is not an embedded browser engine.
        try:
            webbrowser.open(value)
            self.page_label.text = (
                "Requested page:\n" + value +
                "\n\nThis prototype opens pages externally."
            )
            self.notify("Page requested")
        except Exception as exc:
            self.notify("Open failed: " + str(exc))

    def send_action(self, *_args):
        self.notify(
            "Site-specific Send requires native browser integration."
        )

    def file_action(self, *_args):
        self.notify(
            "File upload requires a native file chooser and site integration."
        )

    def copy_page_action(self, *_args):
        self.notify(
            "Copy MW needs an embedded browser to read page contents."
        )

    def paste_action(self, *_args):
        try:
            self.address.text = Clipboard.paste()
            self.notify("Pasted into address field")
        except Exception:
            self.notify("Clipboard unavailable")

    def translate_action(self, *_args):
        value = self.address.text.strip()
        if not value:
            self.notify("Enter an address first")
            return
        url = (
            "https://translate.google.com/translate"
            "?sl=auto&tl=en&u=" + value
        )
        try:
            webbrowser.open(url)
            self.notify("Translation requested")
        except Exception:
            self.notify("Could not open translation")

    def muse_action(self, *_args):
        self.notify(
            "System floating mouse requires Android-native integration."
        )

    def toggle_device(self, *_args):
        self.phone_mode = not self.phone_mode
        self.notify(
            "Phone preview mode" if self.phone_mode else "PC preview mode"
        )

    def setup_action(self, *_args):
        box = BoxLayout(orientation="vertical", spacing=8, padding=8)
        box.add_widget(Label(
            text="DNS preferences are not connected to system DNS."
        ))
        box.add_widget(Label(
            text="System-wide DNS needs Android-supported configuration."
        ))
        close = Button(text="Close", size_hint_y=None, height="40dp")
        box.add_widget(close)

        popup = Popup(
            title="ZodJo Setup",
            content=box,
            size_hint=(0.9, 0.45)
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def copy_address(self, *_args):
        try:
            Clipboard.copy(self.address.text)
            self.notify("Address copied")
        except Exception:
            self.notify("Clipboard unavailable")

    def show_history(self, *_args):
        text = "\n".join(self.history[:20]) or "History is empty."
        self.show_text_popup("History", text)

    def show_bookmarks(self, *_args):
        current = self.address.text.strip()
        if current:
            if current not in self.bookmarks:
                self.bookmarks.insert(0, current)
                write_list(BOOKMARK_FILE, self.bookmarks)
        text = "\n".join(self.bookmarks[:30]) or "No bookmarks."
        self.show_text_popup("Bookmarks", text)

    def show_text_popup(self, title, text):
        box = BoxLayout(orientation="vertical", padding=8, spacing=8)
        field = TextInput(text=text, readonly=True)
        close = Button(
            text="Close",
            size_hint_y=None,
            height="40dp"
        )
        box.add_widget(field)
        box.add_widget(close)
        popup = Popup(
            title=title,
            content=box,
            size_hint=(0.92, 0.8)
        )
        close.bind(on_release=popup.dismiss)
        popup.open()

    def clear_history(self, *_args):
        self.history = []
        write_list(HISTORY_FILE, self.history)
        self.notify("History cleared")

    def save_page(self, *_args):
        path = STATE_DIR / "saved_page.txt"
        path.write_text(
            "Saved address record:\n" + self.address.text,
            encoding="utf-8"
        )
        self.notify("Address record saved, not the full web page")

    def change_text_size(self, *_args):
        self.zoom_level += 10
        if self.zoom_level > 140:
            self.zoom_level = 80
        self.page_label.font_size = str(self.zoom_level / 100 * 14) + "sp"
        self.notify("Text size: " + str(self.zoom_level) + "%")

    def hourly_effect(self, _dt):
        from datetime import datetime
        now = datetime.now()
        key = now.strftime("%Y-%m-%d-%H")
        if now.minute == 0 and now.second < 3 and self._hour_key != key:
            self._hour_key = key
            self.status.text = "ZodJo hourly effect"
            Clock.schedule_once(self.reset_status, 3)


if __name__ == "__main__":
    ZodJoApp().run()
