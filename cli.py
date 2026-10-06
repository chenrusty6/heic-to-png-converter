"""
HEIC to PNG Converter - CLI Interface
Can be invoked directly from command line or via drag-and-drop batch scripts.
"""

import sys
import os
import argparse
from pathlib import Path
from converter import collect_heic_files, batch_convert, SUPPORTED_EXTENSIONS

# Ensure UTF-8 output on Windows consoles
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


def format_size(bytes_num: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"


def main():
    parser = argparse.ArgumentParser(
        description="HEIC to PNG / JPG / WEBP Batch Converter"
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="HEIC/HEIF file(s) or directories to convert."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="Destination directory (default: same folder as original file)"
    )
    parser.add_argument(
        "-f", "--format",
        default="PNG",
        choices=["PNG", "JPG", "WEBP"],
        help="Target image format (default: PNG)"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Number of concurrent conversion threads (default: 4)"
    )
    parser.add_argument(
        "--no-exif",
        action="store_true",
        help="Do not preserve EXIF metadata"
    )
    parser.add_argument(
        "--no-rotate",
        action="store_true",
        help="Do not auto-rotate based on EXIF orientation"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  HEIC to PNG 批次轉換工具 (Command Line)")
    print("=" * 60)

    # Collect files
    files = collect_heic_files(args.inputs)
    total = len(files)

    if total == 0:
        print("\n[!] 未找到任何 HEIC / HEIF 檔案。")
        print(f"    支援的副檔名: {', '.join(SUPPORTED_EXTENSIONS)}")
        sys.exit(1)

    print(f"\n找到 {total} 個待轉換檔案...")
    print(f"目標格式: {args.format.upper()}")
    print(f"輸出目錄: {args.output_dir if args.output_dir else '與原圖相同目錄'}")
    print("-" * 60)

    success_count = 0
    failed_count = 0

    def on_progress(res, current, total_files):
        nonlocal success_count, failed_count
        name = Path(res["input_path"]).name
        if res["success"]:
            success_count += 1
            old_s = format_size(res["original_size"])
            new_s = format_size(res["new_size"])
            print(f"[{current:02d}/{total_files:02d}] 成功: {name} -> {Path(res['output_path']).name} ({old_s} -> {new_s}, {res['elapsed']:.2f}s)")
        else:
            failed_count += 1
            print(f"[{current:02d}/{total_files:02d}] 失敗: {name} (錯誤: {res['error']})")

    results = batch_convert(
        files,
        output_dir=args.output_dir,
        output_format=args.format,
        auto_rotate=not args.no_rotate,
        preserve_exif=not args.no_exif,
        max_workers=args.workers,
        on_file_complete=on_progress
    )

    print("=" * 60)
    print(f"轉換完成! 總計: {total} | 成功: {success_count} | 失敗: {failed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
