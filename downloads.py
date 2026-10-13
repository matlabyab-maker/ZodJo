import threading
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, unquote


BASE = Path("/storage/emulated/0/Yabandeh")
DOWNLOAD_DIR = BASE / "downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


class DownloadManager:
    def __init__(self):
        self.active = {}
        self.lock = threading.Lock()

    def _filename(self, url):
        name = Path(
            unquote(urlparse(url).path)
        ).name

        if not name:
            name = "download.bin"

        name = "".join(
            c for c in name
            if c.isalnum() or c in "._- "
        ).strip()

        return name or "download.bin"

    def download(self, url, callback=None):
        if not url.startswith(("http://", "https://")):
            if callback:
                callback(False, "Invalid URL", None)
            return

        thread = threading.Thread(
            target=self._worker,
            args=(url, callback),
            daemon=True
        )
        thread.start()

    def _worker(self, url, callback):
        try:
            filename = self._filename(url)
            destination = DOWNLOAD_DIR / filename

            counter = 1
            while destination.exists():
                destination = DOWNLOAD_DIR / (
                    f"{Path(filename).stem}_{counter}"
                    f"{Path(filename).suffix}"
                )
                counter += 1

            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=30
            ) as response:
                total = response.headers.get("Content-Length")
                total = int(total) if total else None

                downloaded = 0

                with open(destination, "wb") as output:
                    while True:
                        chunk = response.read(64 * 1024)

                        if not chunk:
                            break

                        output.write(chunk)
                        downloaded += len(chunk)

            message = (
                f"Saved: {destination.name} "
                f"({downloaded} bytes)"
            )

            if total is not None:
                message += f" / expected {total} bytes"

            if callback:
                callback(True, message, str(destination))

        except Exception as error:
            if callback:
                callback(False, str(error), None)
