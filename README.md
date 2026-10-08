<div align="center">

<img src="assets/app_icon_72.png" alt="HEIC to PNG Converter Logo" width="100" height="100" style="border-radius: 20px;">

# HEIC to PNG Converter
### 專為 Windows 打造的 HEIC / HEIF 高品質圖片批次轉換工具

<p align="center">
  <b><a href="README.md">繁體中文</a></b> • <b><a href="README.en.md">English</a></b>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://microsoft.com/windows)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Privacy: 100% Offline](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)](#)
[![Format: HEIC%20to%20PNG%20%7C%20JPG%20%7C%20WEBP](https://img.shields.io/badge/Output-PNG%20%7C%20JPG%20%7C%20WEBP-purple.svg)](#)

<p align="center">
  <b>100% 本地運算 • 極速平行處理 • 完整保留 EXIF • 自動校正拍攝方向 • 支援桌面拖放秒轉</b>
</p>

[✨ 核心亮點](#-核心亮點) •
[📥 下載與安裝](#-下載與使用) •
[📖 使用教學](#-詳細使用教學) •
[💻 開發者指南](#-開發者運行與構建) •
[❓ 常見問題](#-常見問題-faq)

</div>

---

## 💡 為什麼需要這個工具？

當 iPhone 或 iPad 使用者將照片傳送到 Windows 電腦時，經常會遇到 `.heic` 格式打不開、無法直接上傳或進修圖軟體的困擾：
* ❌ **線上轉檔網站**：必須將照片上傳到雲端，有嚴重的**個人私密照外洩隱憂**，且有檔案大小與數量限制。
* ❌ **微軟市集擴充元件**：部分解碼器需額外付費購買。
* ❌ **第三方轉檔軟體**：經常附帶廣告或臃腫套件。

🎉 **本工具提供完美的本地端開源解決方案**：不需連網、無張數限制、多核心極速處理，支援無損 PNG、高品質 JPG 與 WebP！

---

## ✨ 核心亮點

| 特色 | 說明 |
| :--- | :--- |
| 🔒 **100% 本地隱私保障** | 完全在您的電腦本機離線處理，絕不連網，照片安全無虞。 |
| 🌐 **中英雙語介面** | 內建繁體中文與英文雙語切換，可依系統語言自動偵測或隨時手動更換。 |
| ⚡ **雙模式使用體驗** | 支援「視覺化視窗清單操作」與「桌面圖示拖放秒轉」兩種使用方式。 |
| 🧭 **自動方向校正** | 自動辨識手機拍攝方向（Orientation），徹底解決照片橫躺與顛倒問題。 |
| 📷 **完整保留 EXIF 資訊** | 保留原始拍攝日期、時間、相機參數與 GPS 地理資訊。 |
| 🚀 **多核心平行處理** | 採用 Multi-threading 平行加速，上百張照片數秒內即可批次完成。 |
| 🖥️ **高解析度 ClearType** | 支援 Windows Per-Monitor V2 高 DPI 渲染模式，介面字體清晰銳利。 |

---

## 📥 下載與使用

### 🟢 方式一：下載免安裝執行檔（推薦一般使用者）
1. 至本專案的 [Releases 頁面](https://github.com/chenrusty6/heic-to-png-converter/releases) 下載已編譯好的 `HEIC-to-PNG-Converter.exe`。
2. 雙擊即可直接執行，**電腦無需安裝 Python 環境**！

### 🔵 方式二：使用源碼運行（開發者）
請參閱下方 [開發者運行與構建](#-開發者運行與構建)。

---

## 📖 詳細使用教學

### 模式 A：視覺化桌面視窗（適合批次清單管理）
<div align="center">
  <img src="assets/app_icon_72.png" width="48" height="48">
  <p><b>HEIC-to-PNG-App</b></p>
</div>

1. 雙擊開啟 **`HEIC-to-PNG-Converter.exe`**。
2. **加入照片**：
   - 直接將 HEIC 檔案或整個資料夾拖曳至視窗中。
   - 或點擊「+ 選擇檔案...」/「+ 選擇整個資料夾...」。
3. **自訂設定（可選）**：
   - 輸出目錄：預設儲存於原照片旁，亦可自訂目標目錄。
   - 目標格式：支援 **PNG (無損推薦)**、**JPG**、**WEBP**。
   - 可勾選是否保留 EXIF 與自動校正照片旋轉。
4. 點擊 **「⚡ 開始轉換為 PNG」**，即可即時檢視轉換進度與檔案大小變化！

---

### 模式 B：桌面極速拖放（秒轉即成）
<div align="center">
  <img src="assets/heic_dragdrop.png" width="48" height="48">
  <p><b>HEIC-Drag-Drop (原版藍色 + 金色閃電示意)</b></p>
</div>

1. 在檔案總管選取一個或多個 HEIC 照片（或整個資料夾）。
2. 按住滑鼠，**直接拖曳並放開在 `HEIC-Drag-Drop` 圖示上**。
3. 程式會在背景全自動轉換，同名 `.png` 檔案直接儲存在原始照片相同資料夾中！

---

## 💻 開發者運行與構建

### 1. 環境需求
- Python 3.10+
- Windows 10 / 11

### 2. 安裝步驟
```bash
# 複製專案
git clone https://github.com/chenrusty6/heic-to-png-converter.git
cd heic-to-png-converter

# 建立虛擬環境
python -m venv .venv
.\.venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. 運行應用
```bash
# 啟動視窗應用程式
python gui.py

# 或使用命令列 (CLI) 批次轉換
python cli.py "C:\路徑\照片.heic" -o "C:\輸出目錄" -f PNG
```

### 4. 自行打包成 .exe
```bash
python build_exe.py
```
打包完成後，單一可執行檔會輸出於 `dist/HEIC-to-PNG-Converter.exe`。

---

## 📁 專案架構

```text
heic-to-png-converter/
├── assets/                  # 應用程式高解析度圖示與標誌
│   ├── heic_app.ico         # 視窗版原生圖示 (科技藍鏡頭)
│   ├── heic_dragdrop.ico    # 拖放版原生圖示 (藍色鏡頭 + 金色閃電)
│   ├── app_icon_72.png      # 視窗介面專用標誌
│   └── heic_dragdrop.png    # 拖放捷徑高畫質預覽圖
├── docs/                    # GitHub Pages 官方展示頁
│   └── index.html           # 響應式產品展示首頁
├── converter.py             # 圖片轉換核心引擎 (Pillow + pillow-heif 多線程)
├── gui.py                   # 現代化桌面視窗主程式 (TkinterDnD + 高 DPI 優化)
├── i18n.py                  # 中英雙語國際化語言模組
├── cli.py                   # 命令列模式轉換腳本
├── dragdrop_runner.py       # 獨立拖放執行檔入口
├── build_exe.py             # PyInstaller 一鍵打包腳本
├── create_shortcuts.ps1     # 建立桌面原生捷徑腳本
├── requirements.txt         # Python 依賴清單
├── README.md                # 繁體中文說明文件
├── README.en.md             # 英文說明文件 (English Docs)
├── .gitignore               # Git 忽略配置
└── LICENSE                  # MIT 開源授權協議
```

---

## ❓ 常見問題 (FAQ)

#### Q1. 轉出來的 PNG 畫質會變差嗎？
> **不會。** PNG 屬於無損壓縮（Lossless），會 100% 還原 HEIC 的原始色彩與影像細節。

#### Q2. 為什麼有些照片轉出來方向是正的，原本看是橫的？
> 工具內建 **EXIF 方向自動校正**，會自動根據 iPhone 陀螺儀記錄的角度扶正，省去手動旋轉的麻煩。

#### Q3. 如果我要分享給不懂程式的朋友，他需要安裝 Python 嗎？
> **完全不需要。** 只要將 `dist/HEIC-to-PNG-Converter.exe` 傳給他，直接點開就能用！

---

## 📜 開源協議 (License)

本專案基於 [MIT License](LICENSE) 條款開源，歡迎自由使用、修改與分享！
