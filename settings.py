import json
from pathlib import Path


BASE = Path("/storage/emulated/0/Yabandeh")
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)

SETTINGS_FILE = DATA / "settings.json"


DEFAULTS = {
    "search_engine": "Google",
    "display_mode": "PC",
    "text_size": 16,
    "restore_tabs": True,
    "download_folder": str(
        BASE / "downloads"
    ),
}


class SettingsManager:
    def __init__(self):
        self.values = DEFAULTS.copy()
        self.load()

    def load(self):
        try:
            saved = json.loads(
                SETTINGS_FILE.read_text(encoding="utf-8")
            )

            if isinstance(saved, dict):
                self.values.update(saved)

        except (OSError, ValueError, TypeError):
            pass

        return self.values

    def get(self, key, default=None):
        return self.values.get(key, default)

    def set(self, key, value):
        self.values[key] = value
        return self.save()

    def save(self):
        try:
            SETTINGS_FILE.write_text(
                json.dumps(
                    self.values,
                    ensure_ascii=False,
                    indent=2
                ),
                encoding="utf-8"
            )
            return True
        except OSError:
            return False

    def reset(self):
        self.values = DEFAULTS.copy()
        return self.save()
