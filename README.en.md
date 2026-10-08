<div align="center">

<img src="assets/app_icon_72.png" alt="HEIC to PNG Converter Logo" width="100" height="100" style="border-radius: 20px;">

# HEIC to PNG Converter
### High-Performance Offline HEIC / HEIF Batch Image Converter for Windows

<p align="center">
  <b><a href="README.en.md">English</a></b> • <b><a href="README.md">繁體中文</a></b>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://microsoft.com/windows)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)](#)
[![Format: HEIC%20to%20PNG%20%7C%20JPG%20%7C%20WEBP](https://img.shields.io/badge/Output-PNG%20%7C%20JPG%20%7C%20WEBP-purple.svg)](#)

<p align="center">
  <b>100% Offline • Multi-core Parallel Processing • Full EXIF Preservation • Auto-Orientation • Desktop Drag & Drop</b>
</p>

[✨ Highlights](#-key-features) •
[📥 Download & Install](#-download--usage) •
[📖 How to Use](#-how-to-use) •
[💻 Developer Guide](#-developer-guide) •
[❓ FAQ](#-faq)

</div>

---

## 💡 Why This Tool?

When iPhone or iPad photos are transferred to Windows PCs, users frequently encounter unreadable `.heic` files that cannot be opened, shared, or imported into graphic design software:
* ❌ **Online Converters**: Force you to upload private family and personal photos to third-party servers, posing serious **privacy & security risks**, with annoying file size/count limits.
* ❌ **Microsoft Store Codecs**: Often require paid purchases for HEVC/HEIF extensions.
* ❌ **Third-party Freeware**: Bundled with adware, watermarks, or bloated installers.

🎉 **This tool offers a clean, 100% offline open-source solution**: No internet required, no file count limits, multi-threaded high-speed conversion, supporting lossless PNG, high-quality JPG, and modern WebP!

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🔒 **100% Offline & Private** | Fully processed on your local machine. Never connects to the internet; your photos never leave your computer. |
| 🌐 **Bilingual Interface** | Built-in Traditional Chinese and English support with one-click live language switching. |
| ⚡ **Dual Operational Modes** | Choose between the rich **Graphical App** or the instant **Desktop Drag-and-Drop Shortcut**. |
| 🧭 **Automatic Orientation** | Automatically detects camera orientation from metadata, preventing upside-down or sideways photos. |
| 📷 **Full EXIF Preservation** | Keeps original capture dates, times, camera settings, and GPS geolocation coordinates. |
| 🚀 **Multi-Core Parallel Acceleration** | Powered by multithreaded processing, batch converting hundreds of images in seconds. |
| 🖥️ **Crisp High-DPI UI** | Optimized for Windows Per-Monitor V2 High-DPI displays with crystal-clear ClearType rendering. |

---

## 📥 Download & Usage

### 🟢 Option 1: Standalone Portable Executable (Recommended for All Users)
1. Head over to the [GitHub Releases Page](https://github.com/chenrusty6/heic-to-png-converter/releases).
2. Download `HEIC-to-PNG-Converter.exe` (Full GUI) or `HEIC-Drag-Drop.exe` (Instant Drag & Drop).
3. Double-click to launch directly — **No Python installation required!**

### 🔵 Option 2: Run from Source (Developers)
See [Developer Guide](#-developer-guide) below.

---

## 📖 How to Use

### Mode A: Visual Desktop GUI (Best for Batch Organization)
<div align="center">
  <img src="assets/app_icon_72.png" width="48" height="48">
  <p><b>HEIC-to-PNG-App</b></p>
</div>

1. Launch **`HEIC-to-PNG-Converter.exe`**.
2. **Add Photos**:
   - Drag & drop HEIC files or entire folders straight into the window.
   - Or click **"+ Add Files..."** / **"+ Add Folder..."**.
3. **Customize Settings (Optional)**:
   - **Output Folder**: Save directly alongside original photos (default), or pick a custom destination.
   - **Target Format**: Select **PNG (Lossless Recommended)**, **JPG**, or **WEBP**.
   - Toggle EXIF metadata retention and auto-rotation options.
   - Switch language anytime via the 🌐 dropdown in the top-right corner.
4. Click **"⚡ Convert to PNG"** to watch the real-time progress and output paths!

---

### Mode B: Instant Desktop Drag & Drop (Zero-Click Conversion)
<div align="center">
  <img src="assets/heic_dragdrop.png" width="48" height="48">
  <p><b>HEIC-Drag-Drop (Classic Blue Icon + Golden Lightning)</b></p>
</div>

1. Select one or more HEIC files (or an entire folder) in Windows File Explorer.
2. **Drag and release them directly onto the `HEIC-Drag-Drop` icon**.
3. The converter runs automatically in the background, saving identical-name `.png` files into the same folder!

---

## 💻 Developer Guide

### 1. Requirements
- Python 3.10+
- Windows 10 / 11

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/chenrusty6/heic-to-png-converter.git
cd heic-to-png-converter

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Applications
```bash
# Run GUI Application
python gui.py

# Or use Command Line Interface (CLI)
python cli.py "C:\path\to\photo.heic" -o "C:\output_folder" -f PNG
```

### 4. Build Standalone .exe
```bash
python build_exe.py
```
Compiled executables will be output to `dist/HEIC-to-PNG-Converter.exe` and `dist/HEIC-Drag-Drop.exe`.

---

## 📁 Repository Structure

```text
heic-to-png-converter/
├── assets/                  # High-resolution icons and branding assets
│   ├── heic_app.ico         # GUI application Windows icon
│   ├── heic_dragdrop.ico    # Drag-and-drop runner icon with lightning badge
│   ├── app_icon_72.png      # In-app brand header icon
│   └── heic_dragdrop.png    # High-resolution preview
├── docs/                    # GitHub Pages showcase site
│   └── index.html           # Responsive landing page
├── converter.py             # Core multithreaded conversion engine (Pillow + pillow-heif)
├── gui.py                   # High-DPI Tkinter GUI application with DnD
├── i18n.py                  # Bilingual internationalization module (zh-TW & en)
├── cli.py                   # Command-line batch converter
├── dragdrop_runner.py       # Standalone drag-and-drop executable entry point
├── build_exe.py             # Automated PyInstaller packaging script
├── create_shortcuts.ps1     # Native desktop shortcuts creator
├── requirements.txt         # Python package dependencies
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

---

## ❓ FAQ

#### Q1. Does converting to PNG reduce image quality?
> **No.** PNG is a lossless format that reproduces 100% of the pixel data and dynamic range decoded from the original HEIC.

#### Q2. Why are some vertical photos right-side up while they appeared sideways before?
> The tool reads the **EXIF Orientation** tag saved by your smartphone's gyro sensor and automatically rotates the image to its intended angle.

#### Q3. If I share this tool with non-technical friends, do they need Python?
> **Not at all.** Simply send them `HEIC-to-PNG-Converter.exe` from the Releases section. It runs out of the box on Windows with zero setup.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute it.
