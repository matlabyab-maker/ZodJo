from pathlib import Path
import re

BASE = Path("/storage/emulated/0/Yabandeh")
PAGES_DIR = BASE / "pages"


def save_page(content, title="page", extension="txt"):
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    # پاک‌سازی عنوان برای جلوگیری از نام مسیر نامعتبر
    safe_title = str(title or "page").strip()
    safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", safe_title)
    safe_title = safe_title.strip(" .")

    if not safe_title:
        safe_title = "page"

    # پسوند بدون نقطهٔ ابتدایی
    safe_extension = str(extension or "txt").strip().lstrip(".")
    safe_extension = re.sub(r"[^a-zA-Z0-9_-]", "", safe_extension)

    if not safe_extension:
        safe_extension = "txt"

    filename = f"{safe_title}.{safe_extension}"
    destination = PAGES_DIR / filename

    # جلوگیری از بازنویسی فایل موجود
    counter = 1
    while destination.exists():
        destination = PAGES_DIR / (
            f"{safe_title}_{counter}.{safe_extension}"
        )
        counter += 1

    destination.write_text(str(content), encoding="utf-8")
    return str(destination)
