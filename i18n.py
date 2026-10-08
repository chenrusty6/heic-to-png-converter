"""
HEIC to PNG Converter - Internationalization (i18n) Module
Supports Traditional Chinese (zh) and English (en).
"""

import locale
from typing import Dict, Any


def detect_system_language() -> str:
    """Detect system language, defaulting to 'zh' for Chinese locales and 'en' for others."""
    try:
        loc = locale.getdefaultlocale()[0]
        if loc and loc.lower().startswith('zh'):
            return 'zh'
    except Exception:
        pass

    try:
        import ctypes
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0xFF
        # 0x04 is LANG_CHINESE (Taiwan, Hong Kong, PRC, Singapore, Macau)
        if lang_id == 0x04:
            return 'zh'
    except Exception:
        pass

    return 'en'


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "zh": {
        # App Title & Header
        "app_title": "HEIC 轉 PNG 批次圖片轉換器",
        "app_subtitle": "支援 iPhone / iPad 拍攝之 HEIC、HEIF 格式，批次快速轉換為無損 PNG 或高品質 JPG / WebP",
        "lang_switch_label": "語言 / Language:",

        # Drop Zone & Top Buttons
        "drop_hint_dnd": "📂 點擊選擇檔案，或直接將 HEIC / HEIF 檔案或整個資料夾拖曳至此處",
        "drop_hint_nodnd": "📂 點擊下方按鈕選擇 HEIC / HEIF 檔案或資料夾",
        "btn_add_files": "+ 選擇檔案...",
        "btn_add_folder": "+ 選擇整個資料夾...",
        "btn_clear": "🗑️ 清空清單",

        # Settings
        "settings_title": " 輸出與轉換設定 ",
        "lbl_output_dir": "輸出目錄：",
        "rb_same_dir": "保存在原始照片相同資料夾 (推薦)",
        "rb_custom_dir": "指定自訂目錄：",
        "btn_browse": "瀏覽...",
        "lbl_target_format": "目標格式：",
        "cb_preserve_exif": "保留 EXIF 元資訊 (拍攝時間、地點、相機參數)",
        "cb_auto_rotate": "自動校正照片方向 (避免旋轉)",

        # Treeview Headings
        "col_name": "檔案名稱",
        "col_size": "原始大小",
        "col_status": "狀態",
        "col_output": "輸出路徑",

        # Action Bar & Status
        "status_ready": "準備就緒，請拖放或加入 HEIC 檔案",
        "btn_start": "⚡ 開始轉換為 {fmt}",
        "btn_cancel": "取消",
        "btn_open_output": "📁 開啟輸出資料夾",

        # Context Menu
        "menu_remove": "移除選定項目",
        "menu_open_folder": "開啟原圖所在資料夾",

        # Status updates
        "status_waiting": "等待中",
        "status_success": "✅ 完成",
        "status_failed": "❌ 失敗",
        "status_list_count": "清單中共 {total} 個待轉換檔案（剛新增 {new_count} 個）",
        "status_cleared": "清單已清空",
        "status_remaining": "目前剩餘 {count} 個檔案",
        "status_cancelling": "正在取消中，請稍候...",
        "status_converting": "轉換中... {current}/{total} ({pct:.0f}%) - {name}",
        "status_cancelled": "已手動取消！已完成: {sc} 個，失敗: {fc} 個",
        "status_all_done": "🎉 轉換全部完成！成功: {sc} 個，失敗: {fc} 個",
        "size_unknown": "未知",

        # Dialogs
        "dialog_tip": "提示",
        "dialog_no_files": "請先加入至少一個 HEIC/HEIF 檔案！",
        "dialog_no_dest": "請指定有效的自訂輸出目錄！",
        "dialog_error": "錯誤",
        "dialog_mkdir_fail": "無法建立目錄: {e}",
        "dialog_cancelled_title": "已取消",
        "dialog_cancelled_body": "轉換已中止。\n\n成功: {sc} 個\n失敗: {fc} 個",
        "dialog_done_title": "轉換完成",
        "dialog_done_body": "恭喜！所有檔案處理完畢！\n\n成功: {sc} 個\n失敗: {fc} 個",
        "dialog_choose_files": "選擇 HEIC / HEIF 檔案",
        "dialog_choose_folder": "選擇包含 HEIC 檔案的資料夾",
        "dialog_choose_dest": "選擇輸出目錄",
        "filter_heic": "HEIC / HEIF 圖片",
        "filter_all": "所有檔案",

        # DragDrop Runner
        "dd_title": "HEIC 快速拖放轉換器",
        "dd_welcome": "【使用方式】\n\n請直接將一個或多個 HEIC / HEIF 檔案（或整個資料夾），\n用滑鼠拖曳並放開在此圖示上，\n程式就會自動在原目錄生成同名 PNG 檔案！",
        "dd_no_files": "未在拖放的項目中找到任何 HEIC / HEIF 圖片檔案！",
        "dd_done_title": "HEIC 轉換完成",
        "dd_done_body": "🎉 轉換完成！\n\n總計: {total} 個檔案\n成功: {sc} 個\n失敗: {fc} 個\n\n已保存在原照片相同資料夾中。",
    },
    "en": {
        # App Title & Header
        "app_title": "HEIC to PNG Batch Image Converter",
        "app_subtitle": "Fast offline batch converter for iPhone/iPad HEIC/HEIF photos to lossless PNG, JPG, or WebP",
        "lang_switch_label": "Language / 語言:",

        # Drop Zone & Top Buttons
        "drop_hint_dnd": "📂 Click to browse, or drag & drop HEIC / HEIF files / folders here",
        "drop_hint_nodnd": "📂 Click buttons below to select HEIC / HEIF files or folders",
        "btn_add_files": "+ Add Files...",
        "btn_add_folder": "+ Add Folder...",
        "btn_clear": "🗑️ Clear List",

        # Settings
        "settings_title": " Output & Conversion Settings ",
        "lbl_output_dir": "Output Folder:",
        "rb_same_dir": "Save in same folder as source photo (Recommended)",
        "rb_custom_dir": "Custom folder:",
        "btn_browse": "Browse...",
        "lbl_target_format": "Target Format:",
        "cb_preserve_exif": "Preserve EXIF metadata (datetime, GPS, camera details)",
        "cb_auto_rotate": "Auto-rotate orientation based on EXIF",

        # Treeview Headings
        "col_name": "File Name",
        "col_size": "Original Size",
        "col_status": "Status",
        "col_output": "Output Path",

        # Action Bar & Status
        "status_ready": "Ready. Drag & drop or add HEIC files to begin.",
        "btn_start": "⚡ Convert to {fmt}",
        "btn_cancel": "Cancel",
        "btn_open_output": "📁 Open Output Folder",

        # Context Menu
        "menu_remove": "Remove selected item(s)",
        "menu_open_folder": "Open source image folder",

        # Status updates
        "status_waiting": "Waiting",
        "status_success": "✅ Completed",
        "status_failed": "❌ Failed",
        "status_list_count": "Total {total} files in queue ({new_count} newly added)",
        "status_cleared": "List cleared",
        "status_remaining": "{count} files remaining",
        "status_cancelling": "Cancelling, please wait...",
        "status_converting": "Converting... {current}/{total} ({pct:.0f}%) - {name}",
        "status_cancelled": "Cancelled! Completed: {sc}, Failed: {fc}",
        "status_all_done": "🎉 Conversion complete! Success: {sc}, Failed: {fc}",
        "size_unknown": "Unknown",

        # Dialogs
        "dialog_tip": "Notice",
        "dialog_no_files": "Please add at least one HEIC/HEIF file first!",
        "dialog_no_dest": "Please specify a valid custom output directory!",
        "dialog_error": "Error",
        "dialog_mkdir_fail": "Failed to create directory: {e}",
        "dialog_cancelled_title": "Cancelled",
        "dialog_cancelled_body": "Conversion aborted.\n\nSuccess: {sc}\nFailed: {fc}",
        "dialog_done_title": "Conversion Complete",
        "dialog_done_body": "All files processed successfully!\n\nSuccess: {sc}\nFailed: {fc}",
        "dialog_choose_files": "Select HEIC / HEIF Files",
        "dialog_choose_folder": "Select Folder containing HEIC Files",
        "dialog_choose_dest": "Select Output Directory",
        "filter_heic": "HEIC / HEIF Images",
        "filter_all": "All Files",

        # DragDrop Runner
        "dd_title": "HEIC Quick Drag & Drop Converter",
        "dd_welcome": "【How to Use】\n\nDrag and drop one or more HEIC / HEIF files (or an entire folder)\nonto this application icon,\nand it will automatically generate PNG files in the same folder!",
        "dd_no_files": "No HEIC / HEIF image files found in the dropped items!",
        "dd_done_title": "HEIC Conversion Complete",
        "dd_done_body": "🎉 Conversion Complete!\n\nTotal: {total} files\nSuccess: {sc}\nFailed: {fc}\n\nSaved in the original photo's folder.",
    }
}


def t(key: str, lang: str = "zh", **kwargs: Any) -> str:
    """Retrieve translated text by key and format with kwargs."""
    strings = TRANSLATIONS.get(lang, TRANSLATIONS["zh"])
    template = strings.get(key, TRANSLATIONS["zh"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
