# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import ast
import shutil
import sys

# مسیرهای پروژه
BASE = Path("/storage/emulated/0/Yabandeh")
MAIN = BASE / "main.py"
BACKUPS = BASE / "backups"

SOURCE = (
    BACKUPS
    / "main.py_before_page_text_fix_20261013_120409.bak"
)


def stop(message):
    print("\nخطا:", message)
    input("\nبرای خروج Enter بزنید...")
    sys.exit(1)


def main():
    print("=" * 48)
    print("Yabandeh - Restore")
    print("=" * 48)

    print("فایل اصلی:")
    print(MAIN)

    print("\nنسخه پشتیبان موردنظر:")
    print(SOURCE)

    # بررسی وجود فایل‌ها
    if not BASE.is_dir():
        stop("پوشه Yabandeh پیدا نشد.")

    if not MAIN.is_file():
        stop("فایل main.py پیدا نشد.")

    if not SOURCE.is_file():
        stop("نسخه پشتیبان موردنظر پیدا نشد.")

    # بررسی سالم بودن نسخه پشتیبان
    try:
        source_text = SOURCE.read_text(
            encoding="utf-8"
        )
        ast.parse(source_text)

    except Exception as exc:
        stop(
            "نسخه پشتیبان قابل خواندن نیست: "
            + str(exc)
        )

    # نام نسخه ایمنی
    stamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    safety_copy = (
        BACKUPS
        / f"main.py_before_restore_{stamp}.bak"
    )

    temp_file = BASE / "main.py.restore_tmp"

    try:
        # ذخیره نسخه فعلی
        shutil.copy2(MAIN, safety_copy)

        print("\nنسخه فعلی ذخیره شد:")
        print(safety_copy)

        # ساخت فایل موقت
        temp_file.write_text(
            source_text,
            encoding="utf-8"
        )

        # بررسی فایل موقت
        ast.parse(
            temp_file.read_text(
                encoding="utf-8"
            )
        )

        # جایگزینی فایل اصلی
        shutil.copy2(temp_file, MAIN)

        # حذف فایل موقت
        temp_file.unlink(missing_ok=True)

        # بررسی نهایی
        ast.parse(
            MAIN.read_text(
                encoding="utf-8"
            )
        )

        print("\nبازگردانی با موفقیت انجام شد.")
        print("بررسی نحوی main.py موفق بود.")

        print("\nفایل اصلی:")
        print(MAIN)

        print("\nنسخه ایمنی:")
        print(safety_copy)

        print("\nاکنون می‌توانی main.py را اجرا کنی.")
        print("سپس این آدرس را آزمایش کن:")
        print("https://example.com")

    except Exception as exc:
        print("\nخطا هنگام بازگردانی:")
        print(type(exc).__name__, str(exc))

        # تلاش برای برگرداندن نسخه ایمنی
        try:
            if safety_copy.is_file():
                shutil.copy2(safety_copy, MAIN)
                print(
                    "\nنسخه ایمنی به main.py برگردانده شد."
                )
        except Exception as recovery_error:
            print(
                "\nخطا در بازیابی نسخه ایمنی:",
                recovery_error
            )

        try:
            temp_file.unlink(missing_ok=True)
        except Exception:
            pass

    input("\nبرای خروج Enter بزنید...")


if __name__ == "__main__":
    main()