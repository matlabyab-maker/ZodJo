from pathlib import Path
from datetime import datetime
import ast
import shutil

BASE = Path("/storage/emulated/0/Yabandeh")
MAIN = BASE / "main.py"

def stop(message):
    print("\nخطا:", message)
    input("\nبرای خروج Enter بزن...")
    raise SystemExit

try:
    if not MAIN.is_file():
        stop("فایل main.py پیدا نشد.")

    source = MAIN.read_text(encoding="utf-8")

    old_import = "from kivy.uix.button import Button"
    new_import = "from kivy.uix.button import Button as KivyButton"

    if new_import in source and "def Button(*args, **kwargs):" in source:
        print("اصلاح دکمه‌ها قبلاً انجام شده است.")
        input("برای خروج Enter بزن...")
        raise SystemExit

    if old_import not in source:
        stop("خط واردکردن Button پیدا نشد. فایل اصلی تغییر نکرد.")

    if "def _yabandeh_persian_text(" not in source:
        stop("تابع اصلاح فارسی پیدا نشد. فایل اصلی تغییر نکرد.")

    anchor = "class YabandehApp"
    if anchor not in source:
        stop("کلاس اصلی برنامه پیدا نشد. فایل اصلی تغییر نکرد.")

    updated = source.replace(old_import, new_import, 1)

    wrapper = '''
# اصلاح خودکار متن فارسی دکمه‌ها
def Button(*args, **kwargs):
    if "text" in kwargs:
        kwargs["text"] = _yabandeh_persian_text(kwargs["text"])
    elif args:
        args = (_yabandeh_persian_text(args[0]),) + args[1:]
    return KivyButton(*args, **kwargs)


'''

    updated = updated.replace(anchor, wrapper + anchor, 1)
    ast.parse(updated)

    backup_dir = BASE / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = backup_dir / f"main.py_before_buttons_{stamp}.bak"
    shutil.copy2(MAIN, backup)

    temp = BASE / "main.py.tmp"
    temp.write_text(updated, encoding="utf-8")
    ast.parse(temp.read_text(encoding="utf-8"))
    temp.replace(MAIN)

    print("\nاصلاح دکمه‌های فارسی انجام شد.")
    print("نسخه پشتیبان:", backup)
    print("بررسی کد: موفق")

except SystemExit:
    raise
except Exception as error:
    print("\nاصلاح انجام نشد:", repr(error))
finally:
    input("\nبرای خروج Enter بزن...")
