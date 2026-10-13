from pathlib import Path
from datetime import datetime
import ast
import shutil
import sys

base = Path("/storage/emulated/0/Yabandeh")
target = base / "main.py"
font = base / "fonts" / "NotoNaskhArabic.ttf"

if not target.is_file():
    sys.exit("خطا: main.py پیدا نشد؛ فایل تغییر نکرد.")

if not font.is_file():
    sys.exit("خطا: فایل فونت پیدا نشد؛ فایل تغییر نکرد.")

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except Exception as exc:
    sys.exit("کتابخانه‌های فارسی در دسترس نیستند: " + str(exc))

original = target.read_text(encoding="utf-8")

if "def _yabandeh_persian_text(" in original:
    sys.exit("اصلاح فارسی از قبل وجود دارد؛ فایل تغییر نکرد.")

required = [
    "from kivy.uix.label import Label",
    "self.status.text = str(message)",
    "self.page.text = text",
    'self.page.text = "بازکردن صفحه ناموفق بود.\\n" + message',
    'self.page.text = "\\n\\n".join(',
    "self.page.text = self.current_text",
]
missing = [item for item in required if item not in original]
if missing:
    sys.exit("ساختار فایل متفاوت است؛ فایل اصلی تغییر نکرد.")

helper = r'''
def _yabandeh_persian_text(value):
    """آماده‌سازی متن فارسی برای نمایش در Kivy."""
    value = str(value)
    if not any("\u0600" <= char <= "\u06ff" for char in value):
        return value
    try:
        return get_display(arabic_reshaper.reshape(value), base_dir="R")
    except Exception:
        return value

'''

updated = original.replace(
    "from kivy.uix.label import Label\n",
    "from kivy.uix.label import Label\n"
    "import arabic_reshaper\n"
    "from bidi.algorithm import get_display\n",
    1
)

updated = updated.replace(
    'BASE = Path("/storage/emulated/0/Yabandeh")\n',
    helper + 'BASE = Path("/storage/emulated/0/Yabandeh")\n',
    1
)

updated = updated.replace(
    "self.status.text = str(message)",
    "self.status.text = _yabandeh_persian_text(message)",
    1
)

updated = updated.replace(
    "self.page.text = text",
    "self.page.text = _yabandeh_persian_text(text)",
    1
)

updated = updated.replace(
    'self.page.text = "بازکردن صفحه ناموفق بود.\\n" + message',
    'self.page.text = _yabandeh_persian_text("بازکردن صفحه ناموفق بود.\\n" + message)',
    1
)

updated = updated.replace(
    'self.page.text = "\\n\\n".join(',
    'self.page.text = _yabandeh_persian_text("\\n\\n".join(',
    1
)

updated = updated.replace(
    '                for item in items[:100]\n            ) or "تاریخچه خالی است."',
    '                for item in items[:100]\n            ) or "تاریخچه خالی است.")',
    1
)

updated = updated.replace(
    "self.page.text = self.current_text",
    "self.page.text = _yabandeh_persian_text(self.current_text)",
    1
)

try:
    ast.parse(updated)
except SyntaxError as exc:
    sys.exit("بررسی کد ناموفق بود؛ فایل اصلی تغییر نکرد.\n" + str(exc))

backup_dir = base / "backups"
backup_dir.mkdir(parents=True, exist_ok=True)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = backup_dir / ("main.py_before_persian_" + stamp + ".bak")
shutil.copy2(target, backup)

temp = base / "main.py.persian_tmp"
temp.write_text(updated, encoding="utf-8")

try:
    ast.parse(temp.read_text(encoding="utf-8"))
    temp.replace(target)
except Exception:
    if temp.exists():
        temp.unlink()
    shutil.copy2(backup, target)
    sys.exit("ذخیره ناموفق بود؛ نسخهٔ پشتیبان بازگردانده شد.")

print("اصلاح متن فارسی انجام شد.")
print("نسخه پشتیبان:", backup)
print("بررسی نحوی: موفق")
print("حالا main.py را در Pydroid اجرا کن.")
