import json
from pathlib import Path
from datetime import datetime


BASE = Path("/storage/emulated/0/Yabandeh")
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)


class TabManager:
    def __init__(self):
        self.tabs = []
        self.active_index = -1
        self.create_tab("")

    def create_tab(self, url=""):
        tab = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "url": url,
            "title": "New Tab",
        }
        self.tabs.append(tab)
        self.active_index = len(self.tabs) - 1
        return tab

    def close_tab(self, index):
        if 0 <= index < len(self.tabs):
            self.tabs.pop(index)

            if not self.tabs:
                self.create_tab("")
            else:
                self.active_index = min(
                    self.active_index,
                    len(self.tabs) - 1
                )

    def switch_tab(self, index):
        if 0 <= index < len(self.tabs):
            self.active_index = index
            return self.tabs[index]
        return None

    def update_active(self, url, title=None):
        if self.active_index < 0:
            self.create_tab(url)

        self.tabs[self.active_index]["url"] = url

        if title:
            self.tabs[self.active_index]["title"] = title

    def get_active(self):
        if 0 <= self.active_index < len(self.tabs):
            return self.tabs[self.active_index]
        return None

    def save(self):
        path = DATA / "tabs.json"
        try:
            path.write_text(
                json.dumps(
                    {
                        "tabs": self.tabs,
                        "active_index": self.active_index
                    },
                    ensure_ascii=False,
                    indent=2
                ),
                encoding="utf-8"
            )
            return True
        except OSError:
            return False

    def restore(self):
        path = DATA / "tabs.json"

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.tabs = data.get("tabs", [])
            self.active_index = data.get("active_index", 0)

            if not self.tabs:
                self.create_tab("")
            else:
                self.active_index = max(
                    0,
                    min(self.active_index, len(self.tabs) - 1)
                )
            return True
        except (OSError, ValueError, TypeError):
            self.tabs = []
            self.active_index = -1
            self.create_tab("")
            return False
