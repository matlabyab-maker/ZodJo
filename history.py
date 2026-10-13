import json
from pathlib import Path
from datetime import datetime

BASE = Path("/storage/emulated/0/Yabandeh")
FILE = BASE / "data" / "history.json"


class HistoryManager:
    def __init__(self):
        FILE.parent.mkdir(parents=True, exist_ok=True)
        if not FILE.exists():
            self._save([])

    def _load(self):
        try:
            data = json.loads(FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, ValueError, TypeError):
            return []

    def _save(self, items):
        FILE.parent.mkdir(parents=True, exist_ok=True)
        FILE.write_text(
            json.dumps(items, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add(self, url, title=""):
        items = self._load()
        items.insert(0, {
            "url": str(url),
            "title": str(title or url),
            "time": datetime.now().isoformat(timespec="seconds")
        })
        self._save(items[:1000])
        return True

    def get_all(self):
        return self._load()
