"""
HEIC Drag & Drop Standalone Quick Converter Runner
Converts dropped files directly to PNG in place.
Supports bilingual prompts (Traditional Chinese & English) based on system locale.
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# DPI Awareness
try:
    import ctypes
    ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except Exception:
    pass

import converter
import i18n


def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    lang = i18n.detect_system_language()

    # Set icon if available
    base_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    ico_path = base_dir / "assets" / "heic_dragdrop.ico"
    if ico_path.exists():
        try:
            root.iconbitmap(str(ico_path))
        except Exception:
            pass

    args = sys.argv[1:]
    if not args:
        messagebox.showinfo(
            i18n.t("dd_title", lang=lang),
            i18n.t("dd_welcome", lang=lang)
        )
        sys.exit(0)

    # Collect files
    files = converter.collect_heic_files(args)
    if not files:
        messagebox.showwarning(
            i18n.t("dialog_tip", lang=lang),
            i18n.t("dd_no_files", lang=lang)
        )
        sys.exit(0)

    # Run conversion
    results = converter.batch_convert(
        files,
        output_dir=None,  # Same directory as source
        output_format="PNG",
        auto_rotate=True,
        preserve_exif=True,
        max_workers=min(8, os.cpu_count() or 4)
    )

    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count

    msg = i18n.t(
        "dd_done_body",
        lang=lang,
        total=len(results),
        sc=success_count,
        fc=fail_count
    )
    messagebox.showinfo(i18n.t("dd_done_title", lang=lang), msg)


if __name__ == "__main__":
    main()
