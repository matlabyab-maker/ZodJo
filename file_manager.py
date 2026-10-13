from pathlib import Path
import shutil

BASE = Path("/storage/emulated/0/Yabandeh")
FILES = BASE / "files"
DOWNLOADS = BASE / "downloads"
PAGES = BASE / "pages"


class FileManager:
    def __init__(self):
        for folder in (FILES, DOWNLOADS, PAGES):
            folder.mkdir(parents=True, exist_ok=True)

    def list_files(self, category="files"):
        folders = {
            "files": FILES,
            "downloads": DOWNLOADS,
            "pages": PAGES
        }

        if category not in folders:
            raise ValueError("دسته‌بندی نامعتبر است")

        folder = folders[category]
        result = []

        for item in sorted(folder.iterdir()):
            result.append({
                "name": item.name,
                "path": str(item),
                "is_dir": item.is_dir(),
                "size": item.stat().st_size if item.is_file() else 0
            })

        return result

    def copy_file(self, source, destination):
        source = Path(source)
        destination = Path(destination)

        if not source.is_file():
            raise FileNotFoundError(str(source))

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return str(destination)

    def move_file(self, source, destination):
        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            raise FileNotFoundError(str(source))

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        return str(destination)

    def delete_file(self, path):
        path = Path(path)

        if not path.exists():
            return False

        # فقط فایل را حذف می‌کند؛ پوشه‌ها را حذف نمی‌کند.
        if not path.is_file():
            raise IsADirectoryError(str(path))

        path.unlink()
        return True

    def file_size(self, path):
        path = Path(path)
        if not path.is_file():
            return 0
        return path.stat().st_size
