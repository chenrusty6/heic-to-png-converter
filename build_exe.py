"""
Build script to compile HEIC to PNG Converter into standalone Windows executables.
"""

import sys
import subprocess
from pathlib import Path

base_dir = Path(__file__).resolve().parent
pyinstaller_exe = base_dir / ".venv" / "Scripts" / "pyinstaller.exe"

print("=" * 60)
print("Building HEIC to PNG Converter Standalone Executables")
print("=" * 60)

# 1. Build GUI Executable
cmd_gui = [
    str(pyinstaller_exe),
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--name", "HEIC-to-PNG-Converter",
    "--icon", str(base_dir / "assets" / "heic_app.ico"),
    "--add-data", f"{base_dir / 'assets'};assets",
    "--collect-all", "tkinterdnd2",
    "--collect-all", "pillow_heif",
    str(base_dir / "gui.py"),
]

print("\n[1/2] Compiling GUI application...")
res1 = subprocess.run(cmd_gui, cwd=str(base_dir))
if res1.returncode != 0:
    print("[!] GUI Compilation failed.")
    sys.exit(1)

# 2. Build Drag-Drop Runner Executable
cmd_dd = [
    str(pyinstaller_exe),
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--name", "HEIC-Drag-Drop",
    "--icon", str(base_dir / "assets" / "heic_dragdrop.ico"),
    "--add-data", f"{base_dir / 'assets'};assets",
    "--collect-all", "pillow_heif",
    str(base_dir / "dragdrop_runner.py"),
]

print("\n[2/2] Compiling Drag-Drop Runner...")
res2 = subprocess.run(cmd_dd, cwd=str(base_dir))
if res2.returncode != 0:
    print("[!] Drag-Drop Compilation failed.")
    sys.exit(1)

print("\nAll compilations completed successfully!")
