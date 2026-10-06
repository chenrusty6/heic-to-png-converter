"""
HEIC Drag & Drop Standalone Quick Converter Runner
Converts dropped files directly to PNG in place.
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


def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window

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
            "HEIC 快速拖放轉換器",
            "【使用方式】\n\n請直接將一個或多個 HEIC / HEIF 檔案（或整個資料夾），\n用滑鼠拖曳並放開在此圖示上，\n程式就會自動在原目錄生成同名 PNG 檔案！"
        )
        sys.exit(0)

    # Collect files
    files = converter.collect_heic_files(args)
    if not files:
        messagebox.showwarning(
            "提示",
            "未在拖放的項目中找到任何 HEIC / HEIF 圖片檔案！"
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

    msg = f"🎉 轉換完成！\n\n總計: {len(results)} 個檔案\n成功: {success_count} 個\n失敗: {fail_count} 個\n\n已保存在原照片相同資料夾中。"
    messagebox.showinfo("HEIC 轉換完成", msg)


if __name__ == "__main__":
    main()
