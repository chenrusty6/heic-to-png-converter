"""
HEIC to PNG Converter - Core Engine
Handles conversion of HEIC/HEIF images to PNG (and other formats)
with EXIF metadata preservation, auto-rotation, and multithreading.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps
import pillow_heif

# Register HEIF opener with Pillow so Image.open handles HEIC files natively
pillow_heif.register_heif_opener()

SUPPORTED_EXTENSIONS = {'.heic', '.heif', '.hif'}


def is_heic_file(path: str) -> bool:
    """Check if the given file has a HEIC/HEIF extension."""
    return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS


def collect_heic_files(paths: List[str]) -> List[str]:
    """
    Given a list of file and/or directory paths, collect all unique HEIC/HEIF files.
    """
    collected = []
    seen = set()

    for item in paths:
        p = Path(item)
        if not p.exists():
            continue

        if p.is_file():
            if p.suffix.lower() in SUPPORTED_EXTENSIONS:
                abs_path = str(p.resolve())
                if abs_path not in seen:
                    seen.add(abs_path)
                    collected.append(abs_path)
        elif p.is_dir():
            for root, _, files in os.walk(p):
                for f in files:
                    if Path(f).suffix.lower() in SUPPORTED_EXTENSIONS:
                        full_path = str(Path(root, f).resolve())
                        if full_path not in seen:
                            seen.add(full_path)
                            collected.append(full_path)

    return collected


def convert_single_file(
    input_path: str,
    output_dir: Optional[str] = None,
    output_format: str = "PNG",
    auto_rotate: bool = True,
    preserve_exif: bool = True,
    png_compression: int = 6,
) -> Dict[str, Any]:
    """
    Convert a single HEIC file to PNG (or specified target format).

    Returns a dictionary with result details:
    {
        "success": bool,
        "input_path": str,
        "output_path": Optional[str],
        "original_size": int,
        "new_size": int,
        "elapsed": float,
        "error": Optional[str]
    }
    """
    start_time = time.time()
    in_p = Path(input_path)

    if not in_p.exists():
        return {
            "success": False,
            "input_path": input_path,
            "output_path": None,
            "original_size": 0,
            "new_size": 0,
            "elapsed": 0.0,
            "error": "檔案不存在"
        }

    original_size = in_p.stat().st_size

    # Determine destination folder and path
    ext = output_format.lower()
    if ext == "jpeg":
        ext = "jpg"

    dest_folder = Path(output_dir) if output_dir else in_p.parent
    dest_folder.mkdir(parents=True, exist_ok=True)
    out_p = dest_folder / f"{in_p.stem}.{ext}"

    try:
        with Image.open(input_path) as img:
            # Extract EXIF if requested
            exif_bytes = None
            if preserve_exif:
                exif_bytes = img.info.get("exif")

            # Handle EXIF orientation transposition
            if auto_rotate:
                img = ImageOps.exif_transpose(img)

            # Ensure image mode is compatible with target format
            fmt = output_format.upper()
            if fmt == "PNG":
                # PNG supports RGBA, RGB, L, etc.
                if img.mode not in ("RGB", "RGBA", "L", "LA"):
                    img = img.convert("RGBA" if "A" in img.mode else "RGB")
                
                save_kwargs = {
                    "format": "PNG",
                    "compress_level": png_compression,
                    "optimize": False,
                }
                if preserve_exif and exif_bytes:
                    save_kwargs["exif"] = exif_bytes
                
                img.save(str(out_p), **save_kwargs)

            elif fmt in ("JPEG", "JPG"):
                if img.mode != "RGB":
                    img = img.convert("RGB")
                save_kwargs = {
                    "format": "JPEG",
                    "quality": 95,
                    "optimize": True,
                }
                if preserve_exif and exif_bytes:
                    save_kwargs["exif"] = exif_bytes
                img.save(str(out_p), **save_kwargs)

            elif fmt == "WEBP":
                save_kwargs = {
                    "format": "WEBP",
                    "quality": 95,
                }
                if preserve_exif and exif_bytes:
                    save_kwargs["exif"] = exif_bytes
                img.save(str(out_p), **save_kwargs)

            else:
                img.save(str(out_p), format=fmt)

        new_size = out_p.stat().st_size
        elapsed = time.time() - start_time

        return {
            "success": True,
            "input_path": str(in_p),
            "output_path": str(out_p),
            "original_size": original_size,
            "new_size": new_size,
            "elapsed": elapsed,
            "error": None
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "input_path": str(in_p),
            "output_path": None,
            "original_size": original_size,
            "new_size": 0,
            "elapsed": elapsed,
            "error": str(e)
        }


def batch_convert(
    file_paths: List[str],
    output_dir: Optional[str] = None,
    output_format: str = "PNG",
    auto_rotate: bool = True,
    preserve_exif: bool = True,
    max_workers: int = 4,
    on_file_complete: Optional[Callable[[Dict[str, Any], int, int], None]] = None,
    cancel_flag: Optional[Callable[[], bool]] = None
) -> List[Dict[str, Any]]:
    """
    Convert multiple HEIC files in parallel using a ThreadPoolExecutor.
    
    on_file_complete: callback(result_dict, completed_count, total_count)
    cancel_flag: callable returning True if cancellation requested.
    """
    total = len(file_paths)
    results = []
    completed_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                convert_single_file,
                f,
                output_dir=output_dir,
                output_format=output_format,
                auto_rotate=auto_rotate,
                preserve_exif=preserve_exif
            ): f
            for f in file_paths
        }

        for future in as_completed(future_map):
            if cancel_flag and cancel_flag():
                # Cancel pending futures
                for f in future_map:
                    f.cancel()
                break

            res = future.result()
            results.append(res)
            completed_count += 1

            if on_file_complete:
                on_file_complete(res, completed_count, total)

    return results
